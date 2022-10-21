import argparse
import json
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from queue import Queue

BLOCK_LEN = 1024
EOM = b'ENDOFMESSAGE___'


class Worker(Thread):
    def __init__(self, client_socket, direction, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.messages = Queue()
        self.socket = client_socket
        self.direction = direction

    def send(self, client_data=None):
        if self.direction:
            client_data['message'] = input(">: ")
            message = json.dumps(client_data).encode('utf-8')
            self.messages.put(message + EOM)
        else:
            data = self.socket.recv(BLOCK_LEN)
            messages = parse_server_messages(data)
            self.messages.put(messages)

    def close(self):
        self.messages.join()

    def run(self) -> None:
        if not self.direction:
            while True:
                message = self.messages.get()
                if message is None:
                    break
                printing_messages(message)
                self.messages.task_done()
            self.messages.task_done()
        else:
            while True:
                message = self.messages.get()
                if message is None:
                    break
                self.socket.send(message)
                self.messages.task_done()
            self.messages.task_done()


def parse_cli_arguments() -> (str, int):
    parser = argparse.ArgumentParser(description='Эхо-сервер')
    parser.add_argument('--host', type=str, default='localhost')
    parser.add_argument('--port', type=int, default=9999)
    return parser.parse_args()


def get_client_name() -> dict:
    user = {}
    print('Введите Ваш ник_нейм')
    user['name'] = input('Ник? >: ')
    return user


def parse_server_messages(server_message: bytes) -> list:
    messages = server_message.split(EOM)[:-1]
    return messages


def printing_messages(messages) -> None:
    for message in messages:
        message = json.loads(message.decode('utf-8'))
        print(f"{message['name']}: {message['message']}")


def main(host: str, port: int) -> None:
    with socket(AF_INET, SOCK_STREAM) as s:
        s.connect((host, port))

        client_data = get_client_name()

        output_tread = Worker(s, direction=True)
        input_tread = Worker(s, direction=False)

        input_tread.start()
        output_tread.start()

        while True:
            output_tread.send(client_data)
            input_tread.send()

            output_tread.close()
            input_tread.close()


if __name__ == '__main__':
    args = parse_cli_arguments()
    main(host=args.host, port=args.port)
