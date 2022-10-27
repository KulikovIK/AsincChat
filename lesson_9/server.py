import argparse
from select import select
from socket import socket, AF_INET, SOCK_STREAM


class Server:

    def __init__(self, host, port):
        self._BLOCK_LEN: int = 1024
        self._host: str = host
        self._port: int = port
        self._connections: list = []


    @staticmethod
    def parse_server_arguments() -> (str, int):
        arguments = argparse.ArgumentParser(description='Server host ip-address and port')
        arguments.add_argument('--host', type=str, default='localhost')
        arguments.add_argument('--port', type=int, default=9999)
        return arguments.parse_args()

    def read_requests(self, read_for: list) -> dict:
        responses = {}

        for read_socket in read_for:
            try:
                request = read_socket.recv(self._BLOCK_LEN)
                responses[read_socket] = request
            except ConnectionResetError:
                print(f'Client is shutdown {read_socket}')
                self._connections.remove(read_socket)
        return responses

    def write_response(self, write_list: list, requests: dict):
        for write_socket in write_list:
            if write_socket in requests:
                try:
                    response = requests[write_socket]
                    for connection in self._connections:
                        connection.send(response)
                except BrokenPipeError:
                    print(f'Client is shutdown {write_socket}')
                    write_socket.close()
                    self._connections.remove(write_socket)

    def start(self):

        with socket(AF_INET, SOCK_STREAM) as server_socket:
            server_socket.bind((self._host, self._port))
            server_socket.listen(5)
            server_socket.settimeout(0.2)
            print('Server is started!')

            while True:

                try:
                    connection, address = server_socket.accept()
                except OSError:
                    pass
                else:
                    print(f'Connection accepted from {address}')
                    self._connections.append(connection)
                finally:

                    timeout = 10

                    try:
                        read_list, write_list, errors = select(self._connections, self._connections, [], timeout)
                    except OSError:
                        pass

                    requests = self.read_requests(read_list)
                    if requests:
                        self.write_response(write_list, requests)


if __name__ == '__main__':
    args = Server.parse_server_arguments()
    server = Server(args.host, args.port)
    server.start()
