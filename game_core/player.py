"""Модуль для работы с игроком"""


class Player:
    """Содержит основные данные, для каждого игрока"""

    def __init__(self, stone_type, is_AI=False):
        self.is_AI = is_AI
        self._hostages_count = 0
        self.stone_type = stone_type
        self.last_move = (-1, -1)

    def add_hostages(self, count):
        self._hostages_count += count

    @property
    def hostages_count(self):
        return self._hostages_count

    def reset(self):
        self._hostages_count = 0
        self.last_move = (-1, -1)

    def __str__(self):
        stone_name = str(self.stone_type)
        if 'White' in stone_name:
            return 'черный'
        elif 'Black' in stone_name:
            return 'белый'
