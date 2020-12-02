from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QLabel, QMessageBox, QSizePolicy

from game_core.game_manager import Game


class Clock:
    def __init__(self, time_limit: int,
                 game: Game, window):
        self._start_time = time_limit
        self._game = game
        self._window = window

        self._timer = QTimer()
        self._timer.timeout.connect(self._timeout)

        self._current_time = time_limit
        self._text_label = QLabel('Время хода: ' + str(self._current_time))

    def _timeout(self):
        self._current_time -= 1
        self._text_label.setText('Время хода: ' + str(self._current_time))

        if self._current_time <= 0:
            self._interception()

    def _interception(self):
        self._game.time_limit()
        self._text_label.setText('Время вышло!')
        self._window.update()

    def restart(self):
        self._current_time = self._start_time

    def get_label(self) -> QLabel:
        self._text_label.setSizePolicy(QSizePolicy.Maximum,
                                       QSizePolicy.Preferred)
        return self._text_label

    def start(self):
        self._timer.start(1000)
