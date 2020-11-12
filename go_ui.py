import sys

from game_core import game_manager as gm
from graphics import game_window


def main(field_size: int):
    app = game_window.qtw.QApplication([])
    white_player = gm.player.Player(gm.stones.WhiteStone)
    black_player = gm.player.Player(gm.stones.BlackStone)

    game = gm.Game(gm.field.FieldParams(field_size),
                   white_player,
                   black_player)

    window = game_window.GameWindow(field_size, 500, game)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main(int(sys.argv[1]))

