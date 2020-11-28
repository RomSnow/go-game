import socket

import game_core.game_params as gp
from web.connect_service import ConnectionService
from web.web_exceptions import WrongConnection


class GuestRoom(ConnectionService):
    def __init__(self, ip_code):
        super().__init__()
        self._host_ip = self._decode(ip_code)

    def set_connection(self) -> gp.GameParams:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        port = 5000
        while True:
            try:
                sock.connect((self._host_ip, port))
                break
            except OSError as e:
                raise WrongConnection

        self._socket = sock

        params_str = self._socket.recv(2048)
        return self._create_params(params_str.decode())

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

    @staticmethod
    def _create_params(params_str: str) -> gp.GameParams:
        data = params_str.split(',')
        if data[0] == '1':
            game_mode = gp.GameModes.local
        elif data[0] == '2':
            game_mode = gp.GameModes.ai
        else:
            game_mode = gp.GameModes.local

        return gp.GameParams(game_mode=game_mode,
                             field_params=gp.FieldParams(int(data[1])),
                             is_time_mode=bool(data[2]),
                             main_player=data[3])


if __name__ == '__main__':
    inp = input()
    room = GuestRoom(inp)
    room.set_connection()
    room.close()
