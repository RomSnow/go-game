import sys

from PyQt5 import QtWidgets as qtw

from graphics.cell_button import CellButton
from game_core import game_manager as gm


class GameWindow(qtw.QWidget):

    def __init__(self, field_size: int, game: gm.Game):
        super().__init__()
        self._game = game
        self._field_buttons = list()
        self._set_ui(field_size)
        self.show()

    def _set_ui(self, field_size):
        main_grid = qtw.QGridLayout()
        main_grid.setSizeConstraint(qtw.QLayout.SetFixedSize)
        self._set_field(field_size, main_grid)
        self._set_menu(main_grid)
        self.setLayout(main_grid)

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

        main_grid.addLayout(field_grid, 0, 0)

    def _set_menu(self, main_grid: qtw.QGridLayout):
        self._move_line = qtw.QLabel(f'Ход игрока: {self._game.current_player}')
        pass_button = qtw.QPushButton('Pass')
        save_button = qtw.QPushButton('Save')
        exit_button = qtw.QPushButton('Exit')
        button_grid = qtw.QGridLayout()

        pass_button.clicked.connect(self._pass_move)
        exit_button.clicked.connect(qtw.qApp.exit)

        button_grid.addWidget(pass_button, 0, 1)
        button_grid.addWidget(save_button, 0, 2)
        button_grid.addWidget(exit_button, 0, 3)

        menu_grid = qtw.QGridLayout()
        menu_grid.addWidget(self._move_line, 0, 0)
        menu_grid.addLayout(button_grid, 0, 1)
        menu_grid.setColumnMinimumWidth(0, 200)

        main_grid.addLayout(menu_grid, 1, 0)

    def _pass_move(self):
        self._game.make_move('pass')
        self.update()

    def update(self):
        for button in self._field_buttons:
            button.redraw()

        self._move_line.setText(f'Ход игрока: {self._game.current_player}')


if __name__ == '__main__':
    app = qtw.QApplication([])
    win = GameWindow(9, None)
    sys.exit(app.exec_())
