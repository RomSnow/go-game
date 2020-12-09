import unittest

from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication

import game_core.game_manager as gm
from game_core.board_managers import ScoreBoardManager
from graphics.game_window import GameWindow
from graphics.main_window import MainWindow


class TestGameWindow(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])
        self.main_window = MainWindow()
        self.main_window.is_debug = True
        self.main_window.score_board.is_debug = True
        self.score_board = ScoreBoardManager('../score_board.txt')
        self.game_window = GameWindow(gm.GameParams(
            field_params=gm.field.FieldParams(9),
            game_mode=gm.GameModes.local,
            is_time_mode=False
        ), self.main_window, score_board=self.score_board)

    def test_move_button(self):
        button = self.game_window.field_buttons[0]
        QTest.mouseClick(button,
                         Qt.LeftButton)

        self.assertTrue(isinstance(
            self.game_window._game.get_stone_on_position(1, 1),
            gm.stones.WhiteStone
        ))

    def test_pass_button(self):
        QTest.mouseClick(self.game_window.pass_button,
                         Qt.LeftButton)

        self.assertFalse(self.game_window._game.get_stone_on_position(1, 1))

    def test_history_button(self):
        QTest.mouseClick(self.game_window.history_button,
                         Qt.LeftButton)

        self.assertTrue(self.game_window.log_window)

    def test_end_game(self):
        QTest.mouseClick(self.game_window.pass_button,
                         Qt.LeftButton)
        QTest.mouseClick(self.game_window.pass_button,
                         Qt.LeftButton)

    def test_exit_button(self):
        QTest.mouseClick(self.game_window.exit_button,
                         Qt.LeftButton)

        self.assertFalse(self.game_window.isVisible())

    def test_time_mode(self):
        self.game_window = GameWindow(gm.GameParams(
            field_params=gm.field.FieldParams(9),
            game_mode=gm.GameModes.local,
            is_time_mode=True,
            second_on_move=1
        ), self.main_window, score_board=self.score_board)
        first_player = self.game_window._game.current_player

        self.game_window.clock._timeout()

        self.assertNotEqual(self.game_window._game.current_player,
                            first_player)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGameWindow)
    unittest.TextTestRunner(verbosity=2).run(suite)
