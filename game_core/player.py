"""Модуль для работы с игроком"""


class Player:
    """Содержит основные данные, для каждого игрока"""

    def __init__(self, stone_type):
        self._hostages_count = 0
        self.stone_type = stone_type
        self.last_move = (-1, -1)

    def add_hostages(self, count):
        self._hostages_count += count
