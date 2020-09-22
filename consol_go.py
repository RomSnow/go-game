import game_core.game_manager as gm
import sys


def main(board_size: list):
    white_player = gm.player.Player(gm.stones.WhiteStone)
    black_player = gm.player.Player(gm.stones.BlackStone)

    game = gm.Game(gm.field.FieldParams(*board_size),
                   white_player, black_player)

    while game.game_is_on:
        move_str = input(f'Ходит {game.current_player}').split()
        move = move_str[0]

        if move == 'print':
            game.print_field()
            continue

        move_params = list(int(i) for i in move_str[1:])
        game.make_move(move, *move_params)

    white_player_points = game.get_point_count(white_player)
    black_player_points = game.get_point_count(black_player)

    if white_player_points > black_player_points:
        winner = 'белый'
    else:
        winner = 'черный'

    print(f'Очки белого игрока: {white_player_points}')
    print(f'Очки черного игрока: {black_player_points}\n')
    print(f'Победил {winner}')

    print('Начать заново? y/n')
    if input() == 'y':
        main(board_size)


if __name__ == '__main__':
    field_size = list(int(i) for i in sys.argv[1:])
    main(field_size)
