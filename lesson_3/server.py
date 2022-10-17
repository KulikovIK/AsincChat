import argparse
import socket
import logging
import log.server_log_config
from log.logger import Log

BLOCK_LEN = 1024
EOM = b'ENDOFMESSAGE___'
LOGGER = logging.getLogger('app.server')


@Log(LOGGER, __name__)
def parse_cli_arguments():
    parser = argparse.ArgumentParser(description="Эхо сервер")
    parser.add_argument('--host', type=str, default='localhost')
    parser.add_argument('--port', type=int, default=9999)
    return parser.parse_args()


@Log(LOGGER, __name__)
def read_message(connection, user_name: bytes = None) -> bytes:
    message = b''
    while len(message) < len(EOM) or message[-len(EOM):] != EOM:
        data = connection.recv(BLOCK_LEN)
        if not data:
            break
        try:
            if not isinstance(data[0], int):
                raise
        except Exception:
            LOGGER.warning('С данными что-то не так')
        message += data
        if user_name:
            return user_name[:-len(EOM)]+b' sad: ' + message
        return message


def main(host, port):
    LOGGER.info('Start app server')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
        try:
            serversocket.bind((host, port))
        except Exception:
            LOGGER.warning('Соединение занято')
            return
        serversocket.listen()

        while True:
            connection, address = serversocket.accept()
            print(f'Соединение установлено с {address}')
            user_name = read_message(connection)
            connection.send(b'Hi! ' + user_name)
            while True:
                data = read_message(connection, user_name)
                if not data:
                    print(f'Cоединение разорвано')
                    break

                print(data.decode('UTF-8')[:-len(EOM)])
                try:
                    sendet = connection.send(data)
                    if sendet > 0:
                        raise
                except Exception:
                    LOGGER.info('Данные не отправлены, возможно разорвано соединение')


if __name__ == '__main__':
    args = parse_cli_arguments()
    main(host=args.host, port=args.port)
