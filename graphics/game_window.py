import sys
from PyQt5 import QtWidgets as qtw

from graphics.cell_button import CellButton


class GameWindow(qtw.QWidget):

    def __init__(self, field_size: int, window_size: int):
        super().__init__()
        self._set_ui(field_size)
        self.show()

    def _set_ui(self, field_size):
        main_grid = qtw.QGridLayout()
        main_grid.setSizeConstraint(qtw.QLayout.SetFixedSize)
        self._set_field(field_size, main_grid)
        self._set_menu(main_grid)
        self.setLayout(main_grid)

    @staticmethod
    def _set_field(field_size: int, main_grid: qtw.QGridLayout):
        field_grid = qtw.QGridLayout()
        field_grid.setSpacing(0)

        for i in range(field_size):
            for j in range(field_size):
                field_grid.addWidget(CellButton((j, i), field_size), i, j)

        main_grid.addLayout(field_grid, 0, 0)

    @staticmethod
    def _set_menu(main_grid: qtw.QGridLayout):
        save_button = qtw.QPushButton('Save')
        exit_button = qtw.QPushButton('Exit')
        menu_grid = qtw.QGridLayout()
        menu_grid.setColumnMinimumWidth(0, 100)

        menu_grid.addWidget(save_button, 0, 4)
        menu_grid.addWidget(exit_button, 0, 5)

        main_grid.addLayout(menu_grid, 1, 0)


if __name__ == '__main__':
    app = qtw.QApplication([])
    win = GameWindow(12, 500)
    sys.exit(app.exec_())
