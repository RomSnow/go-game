import socket

from web.connect_service import ConnectionService
from web.web_exceptions import WrongConnection


class GuestRoom(ConnectionService):
    def __init__(self, ip_code):
        super().__init__()
        self._host_ip = self._decode(ip_code)

    def set_connection(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        port = 5000
        print('Try to connect...')
        while True:
            try:
                sock.connect((self._host_ip, port))
                break
            except OSError as e:
                raise WrongConnection

        print('Connection pass')
        self._socket = sock

    def close(self):
        self._socket.close()

    @staticmethod
    def _decode(ip_code) -> str:
        address = []
        symbols = [ip_code[x:x + 2] for x in range(0, len(ip_code), 2)]
        for sym in symbols:
            count = int(sym[0])
            off = ord(sym[1]) - 65
            num = count * 26 + off
            address.append(str(num))

        return '.'.join(address)


if __name__ == '__main__':
    inp = input()
    room = GuestRoom(inp)
    room.set_connection()
    room.close()
