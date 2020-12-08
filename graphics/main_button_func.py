import time
from queue import Queue
import threading as thr

from PyQt5 import QtWidgets

import game_core.game_manager as gm
from graphics.board_win import ScoreBoardWindow
from graphics.game_window import GameWindow
from web.guest_room import GuestRoom
from web.host_room import HostRoom
from web.web_exceptions import WrongConnection


class ButtonFunc:
    def __init__(self, main_window):
        self.main_window = main_window

    def play_button_func(self):
        game_params = gm.GameParams(
            game_mode=self.main_window.game_mode,
            field_params=gm.field.FieldParams(self.main_window.field_size_spin
                                              .value()),
            main_player=self.main_window.main_player,
            is_time_mode=self.main_window.time_game_check.isChecked(),
            second_on_move=self.main_window.time_on_move.value()
        )
        game_window = GameWindow(game_params, self.main_window,
                                 score_board=self.main_window.score_board)
        self.main_window.hide()

    def game_type_buttons_func(self, clicked_button):
        self.main_window.game_mode = clicked_button.game_type
        if self.main_window.game_mode == gm.GameModes.online:
            self.main_window.connect_button.show()
            self.main_window.create_button.show()
            self.main_window.start_button.hide()
            self.main_window.record_button.hide()
        else:
            self.main_window.connect_button.hide()
            self.main_window.create_button.hide()
            self.main_window.start_button.show()
            self.main_window.record_button.show()
        for button in self.main_window.game_type_buttons:
            if button == clicked_button:
                button.setSizePolicy(QtWidgets.QSizePolicy(
                    QtWidgets.QSizePolicy.Preferred,
                    QtWidgets.QSizePolicy.Preferred))
            else:
                button.setSizePolicy(QtWidgets.QSizePolicy(
                    QtWidgets.QSizePolicy.Maximum,
                    QtWidgets.QSizePolicy.Preferred))

    def color_button_func(self, clicked_button):
        self.main_window.main_player = clicked_button.color
        for button in self.main_window.choose_color_buttons:
            if button == clicked_button:
                button.setSizePolicy(QtWidgets.QSizePolicy(
                    QtWidgets.QSizePolicy.Preferred,
                    QtWidgets.QSizePolicy.Preferred))

            else:
                button.setSizePolicy(QtWidgets.QSizePolicy(
                    QtWidgets.QSizePolicy.Maximum,
                    QtWidgets.QSizePolicy.Preferred))

    def connect_button_func(self):
        address, ok = QtWidgets.QInputDialog.getText(self.main_window,
                                                     'Подключение',
                                                     'Введите код игры:')
        if not ok:
            return

        guest_room = GuestRoom(address)
        try:
            game_params = guest_room.set_connection()
        except WrongConnection:
            msg = QtWidgets.QMessageBox.question(self.main_window, 'Ошибка',
                                                 'Ошибка подключения!',
                                                 QtWidgets.QMessageBox.Ok)
            return

        if guest_room:
            guest_room.send_confirm()
        game_window = GameWindow(game_params, self.main_window, guest_room)
        self.main_window.hide()

    def create_button_func(self):
        host_room = HostRoom()
        address = host_room.get_address_code()

        game_params = gm.GameParams(
            game_mode=self.main_window.game_mode,
            field_params=gm.field.FieldParams(self.main_window.field_size_spin.value()),
            main_player=self.main_window.main_player,
            is_time_mode=self.main_window.time_game_check.isChecked(),
            second_on_move=self.main_window.time_on_move.value()
        )
        out_queue = Queue()
        thread = thr.Thread(target=host_room.wait_connection,
                            args=(game_params, out_queue))
        thread.start()
        try:
            w = AddressOutMessage(address)
        except gm.ExitException:
            host_room.cancel()
            return
        thread.join()

        ans = out_queue.get()
        if ans == 0:
            pass
        if ans == 1:
            msg = QtWidgets.QMessageBox.question(self.main_window, 'Ошибка',
                                                 'Ошибка подключения!',
                                                 QtWidgets.QMessageBox.Ok)
            return

        if host_room:
            host_room.send_confirm()
        game_window = GameWindow(game_params, self.main_window, host_room)
        self.main_window.hide()

    def record_button_func(self):
        self._score_board = ScoreBoardWindow(self.main_window.score_board,
                                             self.main_window)


class AddressOutMessage(QtWidgets.QMessageBox):
    def __init__(self, address: str):
        super().__init__()
        self.setWindowTitle('Подключение')
        self.setText(f'Код игры: {address}')
        self.setInformativeText('Ожидание подключения')
        ext_button = self.addButton('Отмена',
                                    QtWidgets.QMessageBox.RejectRole)
        ok_button = self.addButton('ОК',
                                   QtWidgets.QMessageBox.RejectRole)
        self.exec()

        if self.clickedButton() == ext_button:
            raise gm.ExitException()
