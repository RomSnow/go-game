import os
from threading import Thread

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton

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

        self.clicked.connect(self._on_click)
        self.setStyleSheet(self._get_style_str())

    def _get_style_str(self) -> str:
        size = int(5 / self._field_size * 10)

        left_border_color = \
            'transparent' if self._x == 0 else 'black'
        up_border_color = \
            'transparent' if self._y == 0 else 'black'
        right_border_color \
            = 'transparent' if self._x == self._field_size - 1 else 'black'
        down_border_color \
            = 'transparent' if self._y == self._field_size - 1 else 'black'

        return f'CellButton {{ margin: 0ex;' \
               f'width: {size}ex; ' \
               f'height: {size}ex; ' \
               f'border-style: solid; ' \
               f'border-width: 1px; ' \
               f'border-top-color: {up_border_color}; ' \
               f'border-right-color: {right_border_color}; ' \
               f'border-bottom-color: {down_border_color}; ' \
               f'border-left-color: {left_border_color}; }}'

    def _on_click(self):
        try:
            self._game.make_move('move', self._x, self._y)
            self._game_window.update()
        except gm.exc.BusyPoint:
            pass
        except gm.exc.SuicideMove:
            pass
        except gm.exc.KOException:
            pass
        except gm.exc.IncorrectMove:
            pass
        except gm.exc.WaitingException:
            return

        thread = Thread(target=self._game.wait_online_move(
            self._game_window.threads, self._game_window.is_waiting_complete))
        thread.start()
        self._game_window.timer.start(500)

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
