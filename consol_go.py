import game_core.game_manager as gm
import sys


def main():
    field_size = (int(i) for i in sys.argv[1:])
    game = gm.Game(gm.field.FieldParams(*field_size))

    while game.game_is_on:
        move_str = input().split()
        move = move_str[0]

        if move == 'print':
            game.print_field()
            continue

        move_params = (int(i) for i in move_str[1:])
        game.make_move(move, *move_params)


if __name__ == '__main__':
    main()
