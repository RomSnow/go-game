import time
import unittest

import game_core.game_manager as gm
import game_core.aienemy as ai
from game_core.field import Point


class GameManagerTests(unittest.TestCase):
    white_player = gm.player.Player(gm.stones.WhiteStone)
    black_player = gm.player.Player(gm.stones.BlackStone)

    def test_make_move(self):
        game = gm.Game(gm.field.FieldParams(9),
                       self.white_player, self.black_player, 'white')
        first_player = game.current_player
        game.make_move('pass', 0, 0)
        self.assertNotEqual(game.current_player, first_player)
        game.make_move('move', 1, 1)
        self.assertEqual(game.current_player, first_player)
        self.assertRaises(gm.exc.IncorrectMove, game.make_move, 'asf', 0, 0)

        self.white_player.reset()
        self.black_player.reset()

    def test_end_game(self):
        game = gm.Game(gm.field.FieldParams(9),
                       self.white_player, self.black_player, 'white')
        game.make_move('pass')
        game.make_move('pass')
        self.assertFalse(game.game_is_on)

        self.black_player.reset()
        self.white_player.reset()

    def test_point_counter(self):
        game = gm.Game(gm.field.FieldParams(9),
                       self.white_player, self.black_player, 'white')
        for i in range(1, 10):
            game.make_move('move', 2, i)
            game.make_move('move', 8, i)

        white_player_points = game.get_point_count(self.white_player)
        black_player_points = game.get_point_count(self.black_player)

        self.assertEqual(white_player_points, 9)
        self.assertEqual(black_player_points, 9)

        self.black_player.reset()
        self.white_player.reset()

    def test_ai_score_on_position(self):
        game = gm.Game(gm.field.FieldParams(3), self.white_player,
                       self.black_player, 'white')

        game.make_move('move', 2, 1)
        game.make_move('move', 1, 2)
        game.make_move('move', 3, 2)

        ai_enemy = ai.AIEnemy(self.black_player, game)
        self.assertEqual(ai_enemy.get_cell_attractiveness(Point(1, 1)), 282)

    def test_get_best_move(self):
        game = gm.Game(gm.field.FieldParams(9), self.white_player,
                       self.black_player, 'white')

        game.make_move('move', 2, 1)
        game.make_move('move', 1, 2)
        game.make_move('move', 3, 2)

        ai_enemy = ai.AIEnemy(self.white_player, game)
        best_points = ai_enemy.get_best_move()
        self.assertEqual(best_points, [Point(1, 1)])

    def test_ai_move(self):
        ai_player = gm.player.Player(gm.stones.BlackStone, True)
        game = gm.Game(gm.field.FieldParams(9), self.white_player,
                       ai_player, 'white', True)

        game.make_move('move', 2, 2)
        self.assertEqual(self.white_player, game.current_player)

    def test_ai_incorrect_move(self):
        ai_player = gm.player.Player(gm.stones.BlackStone, True)
        game = gm.Game(gm.field.FieldParams(9), self.white_player,
                       ai_player, 'white', True)

        for x in range(game.field_size):
            for y in range(game.field_size):
                if not game.is_field_filled:
                    try:
                        game.make_move('move', x, y)
                    except (gm.exc.BusyPoint, gm.exc.KOException,
                            gm.exc.SuicideMove):
                        pass

    def test_log(self):
        game = gm.Game(gm.field.FieldParams(5), self.white_player,
                       self.black_player, 'white')
        game.make_move('move', 1, 1)
        self.assertEqual(game.log_manager.get_board_str(), 'белый: move 1 1')
        self.assertEqual(game.log_manager.get_board_name(), 'История действий')

    def test_get_result(self):
        game = gm.Game(gm.field.FieldParams(5), self.white_player,
                       self.black_player, 'white')

        self.assertEqual(game.get_result(), {'Черный': 0,
                                             'Белый': 0,
                                             'Победитель': 'Черный'})

    def test_create_game(self):
        field_par = gm.field.FieldParams(9)
        game = gm.create_game(
            gm.GameParams(game_mode=gm.GameModes.local,
                          field_params=field_par,
                          is_time_mode=False,
                          ))

        self.assertEqual(9, game.field_size)
        self.assertEqual('белый', str(game.current_player))
        self.assertEqual(False, game.is_online_mode)


if __name__ == '__main__':
    unittest.main()
