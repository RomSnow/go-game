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

    def test_end_game(self):
        game = gm.Game(gm.field.FieldParams(9, 9),
                       self.white_player, self.black_player)
        game.make_move('pass')
        game.make_move('pass')
        self.assertFalse(game.game_is_on)


if __name__ == '__main__':
    unittest.main()
