import argparse
import socket
import unittest

from lesson_3 import client, server

EOM = client.EOM


class TestClientModule(unittest.TestCase):

    def test_parse_cli_arguments_OK(self):
        r = client.parse_cli_arguments()
        self.assertEqual(r, argparse.Namespace(host='localhost', port=9999))

    def test_read_message_OK(self):
        clientsocet = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocet.connect(('localhost', 9999))

        user_name = '123'
        user_message = '345'

        for i in range(2):
            if i != 0:
                message = user_message.encode('utf-8')
            else:
                message = user_name.encode('utf-8')

            message += EOM
            clientsocet.send(message)
            r = client.read_message(clientsocet).decode()
            if i == 0:
                self.assertEqual(r[:-len(EOM)], f'Hi! {user_name}')
            else:
                self.assertEqual(r[:-len(EOM)], f'{user_name} sad: {user_message}')

        clientsocet.close()


if __name__ == '__main__':
    unittest.main()
