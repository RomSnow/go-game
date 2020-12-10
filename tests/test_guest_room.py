import socket
import unittest
from queue import Queue
from threading import Thread

import game_core.game_manager as gm
from web.flag import Flag
from web.guest_room import GuestRoom
from web.host_room import HostRoom


class GuestRoomCases(unittest.TestCase):
    def setUp(self):
        host_room = HostRoom()
        self.ip_code = host_room.get_address_code()
        self.ip = host_room.ip
        host_room.close()

    def thread_connect(self):
        self.guest_room.set_connection()

    def set_connection(self, game_params=None):
        self.con_sock = socket.create_server((self.ip, 5000))
        self.guest_room = GuestRoom(self.ip_code)
        thread = Thread(target=self.thread_connect)
        thread.start()
        self.con, addr = self.con_sock.accept()
        self.con.sendall(str(game_params).encode())
        thread.join()

    def close_connection(self):
        self.con.close()
        self.con_sock.close()
        self.guest_room.close()

    def test_connection(self):
        self.set_connection(gm.GameParams(
            game_mode=gm.GameModes.online,
            field_params=gm.field.FieldParams(9),
            is_time_mode=False))
        self.close_connection()

    def test_send_move(self):
        self.set_connection()
        self.guest_room.send_move('move', gm.field.Point(1, 1))
        move = self.con.recv(2048)
        self.assertEqual(move, b'move 1 1')
        self.close_connection()

    def test_wait_move(self):
        self.set_connection()

        self.con.sendall(b'move 2 2')
        flag = Flag()
        flag.is_up = True
        move = self.guest_room.wait_move(flag)

        self.assertEqual('move 2 2', move)

        self.close_connection()

    def test_wait_confirm(self):
        self.set_connection()

        self.con.sendall(b'ok')

        flag = Flag()
        flag.is_up = True
        queue = Queue()
        self.guest_room.wait_confirm(queue, flag)

        self.assertFalse(flag)
        self.assertEqual(queue.get(), 'ok')

        self.close_connection()


if __name__ == '__main__':
    unittest.main()
