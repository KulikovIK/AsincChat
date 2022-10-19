import argparse
from select import select
from socket import socket, AF_INET, SOCK_STREAM

BLOCK_LEN = 1024


def parse_serv_arguments() -> (str, int):
    parser = argparse.ArgumentParser(description='Эхо-сервер')
    parser.add_argument('--host', type=str, default='localhost')
    parser.add_argument('--port', type=int, default=9999)
    return parser.parse_args()


def read_requests(read_clients: list, all_clients: list) -> dict:
    responses = {}

    for sock in read_clients:
        try:
            data = sock.recv(BLOCK_LEN).decode('utf-8')
            responses[sock] = data
        except:
            print(f'Клиент {sock.fileno()} {sock.getpeername()} отключился')
            all_clients.remove(sock)
    return responses


def write_responses(requests: dict, write_client: list, all_clients: list) -> list:
    for sock in write_client:
        if sock in requests:
            try:
                response = requests[sock].encode('utf-8')
                for client in all_clients:
                    client.send(response)
            except Exception:
                print(f'Клиент {sock.fileno()} {sock.getpeername()} отключился')
                all_clients.remove(sock)
    return all_clients


def mainloop(host: str, port: int) -> None:
    clients = []

    with socket(AF_INET, SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(5)
        s.settimeout(0.2)

        while True:
            try:
                connection, address = s.accept()
            except OSError as e:
                pass
            else:
                print(f'Поступило соединение от {address}')
                clients.append(connection)
            finally:
                wait = 10
                r = []
                w = []
                try:
                    r, w, e = select(clients, clients, [], wait)
                except:
                    pass

                requests = read_requests(r, clients)
                if requests:
                    clients = write_responses(requests, w, clients)


if __name__ == '__main__':
    args = parse_serv_arguments()
    mainloop(host=args.host, port=args.port)
