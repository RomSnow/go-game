import socket
# import web.web_exceptions as web_exc


class HostRoom:
    def __init__(self):
        self._ip = self._get_my_ip()
        self._socket = self._init_socket()

    def _init_socket(self) -> socket.socket:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        port = 5000
        try:
            sock.bind((self._ip, port))
        except OSError:
            pass
            # raise web_exc.WrongConnection

        return sock

    def wait_connection(self) -> bool:
        print("Waiting connection...")
        self._socket.listen(1)
        self._socket.accept()
        print("Connection passed!")
        return True

    @staticmethod
    def _get_my_ip() -> str:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("google.com", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip

    def get_address_code(self) -> str:
        address = self._ip.split('.')
        code_str = ''

        for sym in address:
            num = int(sym)
            count = num // 26
            off = num % 26
            code_str += str(count) + chr(65 + off)

        return code_str

    def close(self):
        self._socket.close()


if __name__ == '__main__':
    room = HostRoom()
    print(room.get_address_code())
    room.wait_connection()
    room.close()
