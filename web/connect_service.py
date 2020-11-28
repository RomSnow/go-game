import socket
import time

from game_core.field import Point
from web.web_exceptions import WrongConnection


class ConnectionService:
    def __init__(self):
        self._socket = socket.socket()

    def send_move(self, move: str, point: Point = Point(0, 0)):
        if move == 'pass':
            send_str = 'pass'
        else:
            send_str = f'{move} {point.x} {point.y}'
        self._try_to_send(send_str.encode())

    def wait_move(self) -> str:
        in_str = self._socket.recv(2048)
        if not in_str:
            raise WrongConnection
        return in_str.decode()

    def send_exit(self):
        self._try_to_send('exit'.encode())

    def close(self):
        self._socket.close()

    def _try_to_send(self, msg: bytes):
        try_count = 0
        while True:
            try:
                self._socket.sendall(msg)
                break
            except OSError:
                if try_count > 5:
                    raise WrongConnection
                time.sleep(20)
                try_count += 1