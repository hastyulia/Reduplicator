import socket
import sys
import unittest
import proxy_server
from unittest import mock


class ProxyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fake_html = """
        <noscript>
            <div class="tag-home__item">
                Поисковая система.
                <span class="hide--screen-xs">
                <a class="tag-home__link">Узнайте больше<a>
            </div>
        </noscript>
        """
        self.fake_html_result = """
        <noscript>
            <div class="tag-home__item">
                Поисковая--хуёисковая система--хуистема.
                <span class="hide--screen-xs">
                <a class="tag-home__link">Узнайте--хюзнайте больше--хуёльше<a>
            </div>
        </noscript>
        """

    def test_init(self) -> None:
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        server = proxy_server.Server(connection)
        self.assertEqual(server.prefix, 'шмель')

    def test_get_response(self):
        mock_socket = mock.Mock()
        mock_socket.recv.return_value = ''
        server = proxy_server.Server(mock_socket)
        with mock.patch('socket.socket') as mock_server_socket:
            mock_server_socket.return_value.recv.return_value = b''
            self.assertEqual(server.get_response(
                b'GET /index.py HTTP/1.1\nHost: www.ym.ru'), b'')

    def test_run(self):
        mock_socket = mock.Mock()
        mock_socket.recv.return_value = ''
        server = proxy_server.Server(mock_socket)
        self.assertEqual(server.run(), None)

    def test_listen(self):
        mock_socket = mock.Mock()
        mock_socket.recv.return_value = ''
        with mock.patch('socket.socket') as mock_socket:
            mock_socket.return_value.accept.return_value = ('', -1)
            with mock.patch('proxy_server.Server') as mock_server:
                mock_server.return_value = 'ggg'
                with self.assertRaises(AttributeError):
                    proxy_server.listen()

    def test_reduplicate_response(self):
        mock_socket = mock.Mock()
        mock_socket.recv.return_value = b''
        server = proxy_server.Server(mock_socket)
        with mock.patch('zlib.decompress') as mock_zlib:
            mock_zlib.return_value = b'kol'
            self.assertEqual(server.reduplicate_response(
                b'kot\r\n\r\nkol f charset=UTF-8\r\ns'), b'kot\r\n\r\ns')
