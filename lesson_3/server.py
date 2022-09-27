import argparse
import socket

BLOCK_LEN = 1024
EOM = b'ENDOFMESSAGE___'


def parse_cli_arguments():
    parser = argparse.ArgumentParser(description="Эхо сервер")
    parser.add_argument('--host', type=str, default='localhost')
    parser.add_argument('--port', type=int, default=9999)
    return parser.parse_args()


def read_message(connection, user_name: bytes = None) -> bytes:
    message = b''
    while len(message) < len(EOM) or message[-len(EOM):] != EOM:
        data = connection.recv(BLOCK_LEN)
        if not data:
            break
        assert isinstance(data[0], int), f'С данными что-то не так'
        message += data
        if user_name:
            return user_name[:-len(EOM)]+b' sad: ' + message
        return message


def main(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
        serversocket.bind((host, port))
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
                sendet = connection.send(data)

                assert sendet > 0, 'Данные не отправлены, возможно разорвано соединение'


if __name__ == '__main__':
    args = parse_cli_arguments()
    main(host=args.host, port=args.port)
