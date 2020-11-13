import sys
from PyQt5.QtWidgets import QApplication

from game_core import game_manager as gm
from graphics import game_window


def main(field_size: int):
    app = QApplication([])

    window = game_window.GameWindow(gm.GameParams(
        field_params=gm.field.FieldParams(3),
        game_mode=gm.GameModes.local

    ))
    sys.exit(app.exec_())


if __name__ == '__main__':
    main(int(sys.argv[1]))
