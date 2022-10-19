import argparse
import json
from socket import socket, AF_INET, SOCK_STREAM

BLOCK_LEN = 1024


def parse_cli_arguments() -> (str, int):
    parser = argparse.ArgumentParser(description='Эхо-сервер')
    parser.add_argument('--host', type=str, default='localhost')
    parser.add_argument('--port', type=int, default=9999)
    return parser.parse_args()


def get_client_name() -> dict:
    user = {}
    print('Введите Ваш ник_нейм')
    user['name'] = input('>: ')
    return user


def main(host: str, port: int) -> None:
    with socket(AF_INET, SOCK_STREAM) as s:
        s.connect((host, port))

        client_data = get_client_name()

        while True:
            client_data['message'] = input(">: ")
            if client_data['message'] == 'exit':
                break

            message = json.dumps(client_data).encode('utf-8')
            s.send(message)

            data = s.recv(BLOCK_LEN)
            data = json.loads(data.decode('utf-8'))
            print(f'{data["name"]}: {data["message"]}')


if __name__ == '__main__':
    args = parse_cli_arguments()
    main(host=args.host, port=args.port)
