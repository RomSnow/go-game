import socket
import time
from queue import Queue

from game_core.field import Point
from web.web_exceptions import WrongConnection


class ConnectionService:
    def __init__(self):
        self._connection = None
        self._socket = None
        self._waiting = False

    def send_move(self, move: str, point: Point = Point(0, 0)):
        if move == 'pass':
            send_str = 'pass -1 -1'
        else:
            send_str = f'{move} {point.x} {point.y}'
        self._try_to_send(send_str.encode())

    def send_confirm(self):
        self._try_to_send(b'ok')

    def wait_confirm(self, queue: Queue, exit_flag: bool):
        while True:
            try:
                ans = self._connection.recv(2048)
                if not ans:
                    continue
                break
            except socket.timeout:
                pass

        exit_flag = False
        if ans.decode() != 'ok':
            queue.put(1)
        else:
            queue.put('ok')

    def wait_move(self, exit_flag: bool) -> str:
        self._waiting = True
        while True:
            if not exit_flag:
                raise SystemExit
            try:
                in_str = self._connection.recv(2048)
                if not in_str:
                    time.sleep(2)
                    continue
                break
            except socket.timeout:
                if not self._waiting:
                    self._waiting = False
                    return ''
            except OSError:
                raise WrongConnection

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
                self._connection.sendall(msg)
                break
            except OSError:
                if try_count > 5:
                    raise WrongConnection
                time.sleep(20)
                try_count += 1
