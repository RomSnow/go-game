import unittest

from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication

from graphics.main_window import MainWindow
import game_core.game_manager as gm


class TestMainWindow(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])
        self.main_window = MainWindow()
        self.main_window.is_debug = True

    def test_change_game_mode(self):
        QTest.mouseClick(self.main_window.online_button, Qt.LeftButton)
        self.assertEqual(self.main_window.game_mode, gm.GameModes.online)
        QTest.mouseClick(self.main_window.local_button, Qt.LeftButton)

    def test_color_button(self):
        QTest.mouseClick(self.main_window.black_button, Qt.LeftButton)
        self.assertEqual(self.main_window.main_player, 'black')
        QTest.mouseClick(self.main_window.white_button, Qt.LeftButton)

    def test_play_button(self):
        QTest.mouseClick(self.main_window.start_button, Qt.LeftButton)
        self.assertTrue(self.main_window.game_window, 'black')

    def test_score_button(self):
        QTest.mouseClick(self.main_window.record_button, Qt.LeftButton)
        self.assertTrue(self.main_window.bt_func._score_board)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMainWindow)
    unittest.TextTestRunner(verbosity=2).run(suite)
