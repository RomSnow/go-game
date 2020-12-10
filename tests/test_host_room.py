import socket
import unittest
from queue import Queue

import game_core.game_manager as gm
from web.flag import Flag
from web.host_room import HostRoom


class HostRoomCases(unittest.TestCase):
    def set_connection(self, game_params=None):
        self.con_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host_room = HostRoom()
        self.con_sock.connect((
            self.host_room.ip,
            5000
        ))
        self.host_room.wait_connection(game_params)

    def close_connection(self):
        self.con_sock.close()
        self.host_room.close()

    def test_connection(self):
        self.set_connection(gm.GameParams(
            game_mode=gm.GameModes.online,
            field_params=gm.field.FieldParams(9),
            is_time_mode=False))
        params_str = self.con_sock.recv(2048).decode()
        self.assertTrue(params_str)
        self.close_connection()

    def test_send_move(self):
        self.set_connection()
        self.host_room.send_move('move', gm.field.Point(1, 1))
        move = self.con_sock.recv(2048)
        self.assertEqual(move, b'move 1 1')
        self.close_connection()

    def test_wait_move(self):
        self.set_connection()

        self.con_sock.sendall(b'move 2 2')
        flag = Flag()
        flag.is_up = True
        move = self.host_room.wait_move(flag)

        self.assertEqual('move 2 2', move)

        self.close_connection()

    def test_wait_confirm(self):
        self.set_connection()

        self.con_sock.sendall(b'ok')

        flag = Flag()
        flag.is_up = True
        queue = Queue()
        self.host_room.wait_confirm(queue, flag)

        self.assertFalse(flag)
        self.assertEqual(queue.get(), 'ok')

        self.close_connection()


if __name__ == '__main__':
    unittest.main()
