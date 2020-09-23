import unittest

import game_core.game_manager as gm


class GameManagerTests(unittest.TestCase):
    white_player = gm.player.Player(gm.stones.WhiteStone)
    black_player = gm.player.Player(gm.stones.BlackStone)

    def test_make_move(self):
        game = gm.Game(gm.field.FieldParams(9, 9),
                       self.white_player, self.black_player)
        first_player = game.current_player
        game.make_move('pass', 0, 0)
        self.assertNotEqual(game.current_player, first_player)
        game.make_move('move', 1, 1)
        self.assertEqual(game.current_player, first_player)
        self.assertRaises(gm.exc.IncorrectMove, game.make_move, 'asf', 0, 0)

        self.white_player.reset()
        self.black_player.reset()

    def test_end_game(self):
        game = gm.Game(gm.field.FieldParams(9, 9),
                       self.white_player, self.black_player)
        game.make_move('pass')
        game.make_move('pass')
        self.assertFalse(game.game_is_on)

        self.black_player.reset()
        self.white_player.reset()

    def test_point_counter(self):
        game = gm.Game(gm.field.FieldParams(9, 9),
                       self.white_player, self.black_player)
        for i in range(1, 10):
            game.make_move('move', 2, i)
            game.make_move('move', 8, i)

        white_player_points = game.get_point_count(self.white_player)
        black_player_points = game.get_point_count(self.black_player)

        self.assertEqual(white_player_points, 9)
        self.assertEqual(black_player_points, 9)

        self.black_player.reset()
        self.white_player.reset()


if __name__ == '__main__':
    unittest.main()
