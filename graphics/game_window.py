from queue import Queue
from threading import Thread

from PyQt5 import QtWidgets as qtw
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox

from game_core import game_manager as gm
from game_core.board_managers import ScoreBoardManager
from graphics.board_win import BoardWindow
from graphics.cell_button import CellButton
from graphics.clock import Clock
from web.connect_service import ConnectionService
from web.flag import Flag
from web.guest_room import GuestRoom
from web.web_exceptions import WrongConnection


class GameWindow(qtw.QWidget):

    def __init__(self, game_params: gm.GameParams,
                 main_window: qtw.QMainWindow,
                 connection_service: ConnectionService = None,
                 score_board: ScoreBoardManager = None):
        super().__init__()
        self._main_win = main_window
        self._connection_service = connection_service
        self._score_board = score_board
        self._win_close = False
        self._game_params = game_params
        self._game = gm.create_game(game_params, connection_service)
        self._field_buttons = list()
        self.threads = list()
        self.clock = None
        self.is_waiting = Flag()
        self.exit_flag = False
        self._set_ui(self._game.field_size)
        self.log_window = None
        self.update()

        self._wait_confirm()

        self.show()

    def _set_ui(self, field_size):
        main_grid = qtw.QGridLayout()
        main_grid.setSizeConstraint(qtw.QLayout.SetFixedSize)
        self._set_field(field_size, main_grid)
        self._set_menu(main_grid)

        if self._game_params.is_time_mode:
            self.clock = Clock(self._game_params.second_on_move,
                               self._game, self)
            main_grid.addWidget(self.clock.get_label(), 0, 0)

        self.setLayout(main_grid)

        self.threads_timer = QTimer()
        self.threads_timer.timeout.connect(self._timeout)

    def _set_field(self, field_size: int, main_grid: qtw.QGridLayout):
        field_grid = qtw.QGridLayout()
        field_grid.setSpacing(0)

        for i in range(field_size):
            for j in range(field_size):
                button = CellButton((j, i), field_size, self._game, self)
                self._field_buttons.append(button)
                field_grid.addWidget(
                    button, i, j
                )

        main_grid.addLayout(field_grid, 1, 0)

    def _set_menu(self, main_grid: qtw.QGridLayout):
        self._move_line = qtw.QLabel(
            f'Ход игрока: {self._game.current_player}')
        history_button = qtw.QPushButton('История')
        pass_button = qtw.QPushButton('Пасс')
        exit_button = qtw.QPushButton('Выход')
        button_grid = qtw.QGridLayout()

        history_button.clicked.connect(self._show_logs)
        pass_button.clicked.connect(self._pass_move)
        exit_button.clicked.connect(self.close)

        button_grid.addWidget(pass_button, 0, 1)
        button_grid.addWidget(history_button, 0, 2)
        button_grid.addWidget(exit_button, 0, 3)

        menu_grid = qtw.QGridLayout()
        menu_grid.addWidget(self._move_line, 0, 0)
        menu_grid.addLayout(button_grid, 0, 1)
        menu_grid.setColumnMinimumWidth(0, 200)

        main_grid.addLayout(menu_grid, 2, 0)

    def _pass_move(self):
        if self.is_waiting:
            return
        self._game.make_move('pass')
        self.update()
        if self._game.is_online_mode:
            self.wait_move()

    def _wait_confirm(self):
        if not self._connection_service:
            if self.clock:
                self.clock.start()
            return

        self._move_line.setText('Ожидание второго игрока')
        queue = Queue()
        thread = Thread(target=self._connection_service.wait_confirm,
                        args=(queue, self.is_waiting))
        self.is_waiting.is_up = True
        thread.start()
        self.threads.append((thread, queue))
        self.threads_timer.start(500)

    def _timeout(self):
        if self.threads:
            thread = self.threads.pop()
            if not thread[1].qsize():
                self.threads.append(thread)
            else:
                self.threads_timer.stop()
                thread[0].join()
                ans = thread[1].get()
                if ans == 0:
                    self.update()
                elif ans == 1:
                    self.msg = QMessageBox().question(
                        self,
                        'Уведомление',
                        'Противник вышел!',
                        QMessageBox.Ok
                    )
                    self.close()
                elif ans == 2:
                    self.msg = QMessageBox().question(
                        self,
                        'Уведомление',
                        'Ошибка сети!',
                        QMessageBox.Ok
                    )
                    self.close()
                elif ans == 'ok':
                    if self.clock:
                        self.clock.start()
                    self.is_waiting.is_up = False
                    if isinstance(self._connection_service, GuestRoom):
                        self.wait_move()
                    self._move_line.setText(
                        f'Ход игрока: {self._game.current_player}')

                if self.clock:
                    self.clock.restart()

    def update(self):
        for button in self._field_buttons:
            button.redraw()

        if self.clock:
            self.clock.restart()

        self._move_line.setText(f'Ход игрока: {self._game.current_player}')

        if self.log_window:
            self.log_window.update_text()

        if not self._game.game_is_on:
            self._restart_game()
            if not self._win_close:
                self.update()

    def wait_move(self):
        queue = Queue()
        thread = Thread(target=self._game.wait_online_move,
                        args=(queue, self.is_waiting))
        self.threads.append((thread, queue))
        self.is_waiting.is_up = True
        thread.start()
        self.threads_timer.start(500)

    def _get_player_name(self):
        white_ok = black_ok = False
        white_name = black_name = None
        if self._score_board:
            if (self._game.is_online_mode and
                self._game_params.main_player == 'white') or \
                    not self._game.is_online_mode:
                while True:
                    white_name, white_ok = qtw.QInputDialog. \
                        getText(self, 'Запись результатов',
                                'Введите имя белого игрока\n'
                                '(без пробелов, не более 12 символов):')
                    if (len(white_name) > 12 or len(white_name) < 1
                        or ' ' in white_name) and white_ok:
                        msg = qtw.QMessageBox.question(self, 'Ошибка имени',
                                                       'Неверный формат имени',
                                                       qtw.QMessageBox.Ok)
                        continue
                    break
            if (self._game.is_online_mode and
                self._game_params.main_player == 'black') or \
                    not self._game.is_online_mode:
                while True:
                    black_name, black_ok = qtw.QInputDialog. \
                        getText(self, 'Запись результатов',
                                'Введите имя черного игрока\n'
                                '(без пробелов, не более 12 символов):')
                    if (len(black_name) > 12 or len(black_name) < 1 or
                        ' ' in black_name) and black_ok:
                        msg = qtw.QMessageBox.question(self, 'Ошибка имени',
                                                       'Неверный формат имени',
                                                       qtw.QMessageBox.Ok)
                        continue
                    break

        return white_name, white_ok, black_name, black_ok

    def _restart_game(self):

        white_name, white_ok, black_name, black_ok = self._get_player_name()

        result = self._game.get_result()
        white_str = f'Белый: {result["Белый"]} очков'
        black_str = f'Черный: {result["Черный"]} очков'
        win_str = f'Победитель: {result["Победитель"]} игрок'
        restart_str = 'Начать заново?'

        if white_ok:
            self._score_board.set_player_score(white_name, result["Белый"])
        if black_ok:
            self._score_board.set_player_score(black_name, result["Черный"])

        buttons = (qtw.QMessageBox.Yes | qtw.QMessageBox.No, qtw.QMessageBox.No)

        if self._game.is_online_mode:
            buttons = (qtw.QMessageBox.Ok,)
            restart_str = ''

        result_str = f'{white_str}\n{black_str}\n{win_str}\n{restart_str}'
        reply = qtw.QMessageBox.question(self, 'Restart',
                                         result_str,
                                         *buttons
                                         )

        if reply == qtw.QMessageBox.Yes:
            self.log_window.close()
            self._game = gm.create_game(self._game_params)
            for button in self._field_buttons:
                button.set_game_condition(self._game)

        else:
            self._win_close = True
            self.close()

    def _show_logs(self):
        self.log_window = BoardWindow(self._game.log_manager, self)

    def closeEvent(self, a0) -> None:
        self._main_win.show()

        if self.log_window:
            self.log_window.close()

        if self._game.is_online_mode:
            if self._connection_service.is_open:
                try:
                    self._connection_service.send_move('exit')
                except WrongConnection:
                    pass
            self.is_waiting.is_up = False
            for thread in self.threads:
                thread[0].join()
            self._connection_service.close()

        if self.clock:
            self.clock.stop()
