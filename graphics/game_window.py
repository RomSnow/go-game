import sys

from PyQt5 import QtWidgets as qtw

from game_core import game_manager as gm
from graphics.cell_button import CellButton


class GameWindow(qtw.QWidget):

    def __init__(self, game_params: gm.GameParams,
                 main_window: qtw.QMainWindow):
        super().__init__()
        self._main_win = main_window
        self._win_close = False
        self._game_params = game_params
        self._game = gm.create_game(game_params)
        self._field_buttons = list()
        self._set_ui(self._game.field_size)
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
        exit_button = qtw.QPushButton('Exit')
        button_grid = qtw.QGridLayout()

        pass_button.clicked.connect(self._pass_move)
        exit_button.clicked.connect(self.close)

        button_grid.addWidget(pass_button, 0, 1)
        button_grid.addWidget(exit_button, 0, 2)

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

        if not self._game.game_is_on:
            self._restart_game()
            if not self._win_close:
                self.update()

    def _restart_game(self):
        result = self._game.get_result()
        white_str = f'Белый: {result["Белый"]} очков'
        black_str = f'Черный: {result["Черный"]} очков'
        win_string = f'Победитель: {result["Победитель"]} игрок'
        result_str = f'{white_str}\n{black_str}\n{win_string}\nНачать заново?'

        reply = qtw.QMessageBox.question(self, 'Restart',
                                         result_str,
                                         qtw.QMessageBox.Yes |
                                         qtw.QMessageBox.No,
                                         qtw.QMessageBox.No)
        #
        if reply == qtw.QMessageBox.Yes:
            self._game = gm.create_game(self._game_params)
            for button in self._field_buttons:
                button.set_game_condition(self._game)

        else:
            self._win_close = True
            self.close()

    def closeEvent(self, a0) -> None:
        self._main_win.show()
