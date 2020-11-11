from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton


class CellButton(QPushButton):
    def __init__(self, position: tuple, field_size: int):
        super().__init__()
        self.x = position[0]
        self.y = position[1]
        self._field_size = field_size
        self.clicked.connect(self._on_click)
        self.setStyleSheet(self._get_style_str())

    def _get_style_str(self) -> str:
        size = int(5 / self._field_size * 10)

        left_border_color =\
            'transparent' if self.x == 0 else 'black'
        up_border_color = \
            'transparent' if self.y == 0 else 'black'
        right_border_color \
            = 'transparent' if self.x == self._field_size - 1 else 'black'
        down_border_color \
            = 'transparent' if self.y == self._field_size - 1 else 'black'

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
        self.setIconSize(QSize(300 / self._field_size, 100))


