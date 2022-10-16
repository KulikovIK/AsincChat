import argparse
import socket
import unittest

from lesson_3 import client, server

EOM = server.EOM


class TestServerModule(unittest.TestCase):
    # def tearDown(self) -> None:
    #     self.test_read_message_OK.close()

    def test_parse_cli_arguments_OK(self):
        r = client.parse_cli_arguments()
        self.assertEqual(r, argparse.Namespace(host='localhost', port=9999))

    def test_read_message_OK(self):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind(('localhost', 9999))
        serversocket.listen()

        clientsocet = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocet.connect(('localhost', 9999))

        user_name = '123'.encode('utf-8')
        user_name += EOM
        user_message = '345'.encode('utf-8')
        user_message += EOM

        connection, address = serversocket.accept()

        clientsocet.send(user_name)
        r = server.read_message(connection)
        self.assertEqual(r, user_name)

        clientsocet.send(user_message)
        r = server.read_message(connection, user_name[:-len(EOM)])
        test_message = b' sad: ' + user_message
        self.assertEqual(r, test_message)

        clientsocet.close()
        serversocket.close()


if __name__ == '__main__':
    unittest.main()
