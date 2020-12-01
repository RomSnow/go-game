import socket
import time

import web.web_exceptions as web_exc
from game_core.game_params import GameParams
from web.connect_service import ConnectionService


class HostRoom(ConnectionService):
    def __init__(self):
        super().__init__()
        self._ip = self._get_my_ip()
        self._socket = self._init_socket()
        self._connection = None

    def _init_socket(self) -> socket.socket:
        sock = socket.create_server((self._ip, 5000))
        sock.settimeout(3)
        return sock

    def wait_connection(self, game_params: GameParams = None) -> bool:
        self._socket.listen(1)
        self._waiting = True
        while True:
            try:
                con, address = self._socket.accept()
                break
            except socket.timeout:
                if not self._waiting:
                    self._waiting = True
                    return False

        self._connection = con
        con.sendall(str(game_params).encode())
        return True

    @staticmethod
    def _get_my_ip() -> str:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.connect(('<broadcast>', 0))
        return s.getsockname()[0]

    def get_address_code(self) -> str:
        address = self._ip.split('.')
        code_str = ''

        for sym in address:
            num = int(sym)
            count = num // 26
            off = num % 26
            code_str += str(count) + chr(65 + off)

        return code_str

    def cancel(self):
        self._waiting = False
        time.sleep(3)
        self.close()


if __name__ == '__main__':
    host = HostRoom()
    print(host._get_my_ip())
    host.wait_connection()
    host.close()
