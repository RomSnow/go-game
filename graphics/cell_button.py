from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton

from game_core import game_manager as gm


class CellButton(QPushButton):
    def __init__(self, position: tuple, field_size: int,
                 game: gm.Game):
        super().__init__()
        self._x = position[0]
        self._y = position[1]
        self._field_size = field_size
        self._game = game

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
        self.setIcon(QIcon('black.png'))
        # try:
        #     self._game.make_move('move', self._x, self._y)
        #     current_player = str(self._game.current_player)
        #     if current_player == 'черный':
        #         stone_icon = 'black.png'
        #     else:
        #         stone_icon = 'white.png'
        #
        #     self.setIcon(QIcon(stone_icon))
        #     self.setIconSize(QSize(300 / self._field_size, 100))
        # except Exception:
        #     pass
