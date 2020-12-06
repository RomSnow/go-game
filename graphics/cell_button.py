import os

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QPushButton, QMessageBox, QSizePolicy

from game_core import game_manager as gm


class CellButton(QPushButton):
    def __init__(self, position: tuple, field_size: int,
                 game: gm.Game, game_window):
        super().__init__()
        self._x = position[0] + 1
        self._y = position[1] + 1
        self._field_size = field_size
        self._game = game
        self._game_window = game_window
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.clicked.connect(self._on_click)
        self.setStyleSheet(self._get_style_str())

    def _get_style_str(self) -> str:
        proportion = QApplication.desktop().width() / 1920
        size = int(5 / self._field_size * 100 * proportion)

        left_border_color = \
            'transparent' if self._x == 0 else 'black'
        up_border_color = \
            'transparent' if self._y == 0 else 'black'
        right_border_color \
            = 'transparent' if self._x == self._field_size - 1 else 'black'
        down_border_color \
            = 'transparent' if self._y == self._field_size - 1 else 'black'

        return f'CellButton {{ margin: 0ex;' \
               f'width: {size}px; ' \
               f'height: {size}px; ' \
               f'border-style: solid; ' \
               f'border-width: 1px; ' \
               f'border-top-color: {up_border_color}; ' \
               f'border-right-color: {right_border_color}; ' \
               f'border-bottom-color: {down_border_color}; ' \
               f'border-left-color: {left_border_color}; }}'

    def _on_click(self):
        if self._game_window.is_waiting:
            return
        try:
            self._game.make_move('move', self._x, self._y)
            self._game_window.update()
        except gm.exc.BusyPoint:
            self._game_window.msg = \
                QMessageBox.question(self._game_window,
                                     'Неверный ход',
                                     'Точка занята!',
                                     QMessageBox.Ok)
            return
        except gm.exc.SuicideMove:
            self._game_window.msg = \
                QMessageBox.question(self._game_window,
                                     'Неверный ход',
                                     'Самоубийственный ход!',
                                     QMessageBox.Ok)
            return
        except gm.exc.KOException:
            self._game_window.msg = \
                QMessageBox.question(self._game_window,
                                     'Неверный ход',
                                     'Точка занята!',
                                     QMessageBox.Ok)
            return
        except gm.exc.IncorrectMove:
            self._game_window.msg = \
                QMessageBox.question(self._game_window,
                                     'Неверный ход',
                                     'Точка занята!',
                                     QMessageBox.Ok)
            return
        except gm.exc.WaitingException:
            return

        if self._game.is_online_mode:
            self._game_window.wait_move()

    def redraw(self):
        stone = self._game.get_stone_on_position(self._x, self._y)
        if isinstance(stone, gm.stones.BlackStone):
            stone_icon = 'black.png'
        elif isinstance(stone, gm.stones.WhiteStone):
            stone_icon = 'white.png'
        else:
            stone_icon = ''

        self.setIcon(QIcon(f'{os.path.dirname(__file__)}/{stone_icon}'))
        self.setIconSize(QSize(300 / self._field_size, 100))

    def set_game_condition(self, game: gm.Game):
        self._game = game
