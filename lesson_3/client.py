import argparse
import logging
import socket
import log.client_log_config
from log.logger import Log

BLOCK_LEN: int = 1024
EOM: bytes = b'ENDOFMESSAGE___'
WELCOME_MESSAGE: str = 'Hi! What is your name?'
LOGGER = logging.getLogger('app.client')


@Log(LOGGER, __name__)
def parse_cli_arguments():
    parser = argparse.ArgumentParser(description="Эхо сервер")
    parser.add_argument('--host', type=str, default='localhost')
    parser.add_argument('--port', type=int, default=9999)
    return parser.parse_args()


@Log(LOGGER, __name__)
def read_message(connection) -> bytes:
    message = b''
    while len(message) < len(EOM) or message[-len(EOM):] != EOM:
        try:
            data = connection.recv(BLOCK_LEN)
            if not data:
                raise
        except Exception:
            LOGGER.warning('Ошибка отправки данных. Разрыв соединения с сервером')
            break
        message += data
        return message


def main(host, port):
    LOGGER.info('Start app client')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientsocket:
        clientsocket.connect((host, port))
        print(WELCOME_MESSAGE)

        while True:
            message = input('>').encode('utf-8')
            message += EOM
            clientsocket.send(message)
            response = read_message(clientsocket).decode()
            print(response[:-len(EOM)])


if __name__ == '__main__':
    args = parse_cli_arguments()
    main(host=args.host, port=args.port)
