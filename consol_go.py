import game_core.game_manager as gm
import sys


def main(board_size: list):
    white_player = gm.player.Player(gm.stones.WhiteStone)
    black_player = gm.player.Player(gm.stones.BlackStone)

    game = gm.Game(gm.field.FieldParams(*board_size),
                   white_player, black_player)

    while game.game_is_on:
        move_str = input().split()
        move = move_str[0]

        if move == 'print':
            game.print_field()
            continue

        move_params = (int(i) for i in move_str[1:])
        game.make_move(move, *move_params)


if __name__ == '__main__':
    field_size = list(int(i) for i in sys.argv[1:])
    main(field_size)
