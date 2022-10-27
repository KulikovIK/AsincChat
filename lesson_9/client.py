import argparse
import json
import subprocess
import time
from socket import socket, AF_INET, SOCK_STREAM


class Client:

    def __init__(self, host: str, port: int, client_type: str = 'write'):
        self._BLOCK_LEN: int = 1024
        self._EOM: bytes = b'ENDOFMESSAGE___'
        self._host: str = host
        self._port: int = port
        self._client_type: bool = False if client_type == 'read' else True
        self.user_name: str = ''

    @staticmethod
    def parse_cli_arguments() -> (str, int):
        parser = argparse.ArgumentParser(description='Эхо-клиент')
        parser.add_argument('--host', type=str, default='localhost')
        parser.add_argument('--port', type=int, default=9999)
        parser.add_argument('--type', type=str, default=True)
        return parser.parse_args()

    def get_client_name(self) -> None:
        if self._client_type:
            print('Введите Ваш ник_нейм')
            self.user_name = input('Ник? >: ')
            print()

    def start_chat_process(self) -> None:
        if self._client_type:
            subprocess.Popen('python3 client.py --type=read', shell=True)

    def get_message(self, get_socket: socket) -> None:
        server_message = get_socket.recv(self._BLOCK_LEN)
        messages = self.parse_server_messages(server_message)
        self.printing_messages(messages)

    def send_message(self, send_socket: socket, message: str) -> None:
        client_data = {'user_name': self.user_name, 'message': message}
        encoded_data = json.dumps(client_data).encode('utf-8')
        send_socket.send(encoded_data + self._EOM)

    def parse_server_messages(self, server_message: bytes) -> list:
        messages = server_message.split(self._EOM)[:-1]
        return messages

    def printing_messages(self, messages: list) -> None:
        for message in messages:
            message = json.loads(message.decode('utf-8'))
            print(f"{message['user_name']}: {message['message']}")

    def start(self) -> None:

        with socket(AF_INET, SOCK_STREAM) as s:
            s.connect((self._host, self._port))

            self.get_client_name()
            self.start_chat_process()

            while True:
                if self._client_type:
                    message = input('>: ')
                    if message == '/exit':
                        break

                    self.send_message(s, message)
                    continue

                self.get_message(s)


if __name__ == '__main__':
    args = Client.parse_cli_arguments()
    client = Client(host=args.host, port=args.port, client_type=args.type)
    client.start()
