import re
import sys
import zlib
import socket
import reduplicator
from threading import Thread


class Server(Thread):
    def __init__(self, connection: socket.socket):
        super().__init__()
        self.connection = connection
        self.prefix = 'шмель'

    def run(self) -> None:
        while True:
            request = self.connection.recv(1024)
            if not request:
                break

            response = self.get_response(request)
            self.connection.sendall(response)

        self.connection.shutdown(1)
        self.connection.close()

    def get_response(self, request: bytes) -> bytes:
        request = request.decode('UTF-8')
        host = request.split('\n')[1].split()[1]
        request = re.sub(r'\r\nConnection: [a-z\-]*?\r\n',
                         '\r\nConnection: close\r\n', request)
        request = re.sub(r'\r\nAccept-Encoding: [a-z\-, ]*?\r\n',
                         '\r\nAccept-Encoding: deflate\r\n', request)
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        connection.connect((host, 80))
        connection.send(request.encode('UTF-8'))
        response = b''
        while True:
            html_response = connection.recv(1024)
            response += html_response
            if not html_response:
                break

        connection.close()
        html_text = response.find(b'Content-Type: text/html')
        if (response == b'' or html_text == -1 or
                response.split(b' ')[1] != b'200'):
            return response

        return self.reduplicate_response(response)

    def reduplicate_response(self, response):
        response_split = response.split(b'\r\n\r\n', maxsplit=1)
        charset = response.split(b'charset=')[1].split(b'\r\n')[0].decode(
            'UTF-8')
        gzip_f = response_split[0].find(b'Content-Encoding: deflate')
        if gzip_f != -1:
            decompressed_data = zlib.decompress(response_split[1])
        else:
            decompressed_data = response_split[1]
            rn = decompressed_data.find(b'\r\n')
            if rn != -1:
                decompressed_data = decompressed_data.split(b'\r\n',
                                                            maxsplit=1)[1]

        web_reduplicator = reduplicator.Reduplicator(self.prefix)
        web_reduplicator.reduplicate(decompressed_data.decode(charset))
        reduplicate_response = response_split[0] + b'\r\n\r\n'
        reduplicate_response += web_reduplicator.result.encode('UTF-8')
        return reduplicate_response


def listen() -> None:
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    connection.bind(('0.0.0.0', 17000))
    connection.listen(20)
    while True:
        current_connection, address = connection.accept()
        server = Server(current_connection)
        server.start()


if __name__ == "__main__":
    try:
        listen()
    except KeyboardInterrupt:
        sys.exit(0)
