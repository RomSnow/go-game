"""Модуль для работы с игроком"""


class Player:
    """Содержит основные данные, для каждого игрока"""

    def __init__(self, stone_type, is_AI=False):
        self._is_AI = is_AI
        self._hostages_count = 0
        self._stone_type = stone_type
        self.last_move = (-1, -1)

    def add_hostages(self, count):
        self._hostages_count += count

    @property
    def stone_type(self):
        return self._stone_type

    @property
    def is_ai(self):
        return self._is_AI

    @property
    def hostages_count(self):
        return self._hostages_count

    def set_ai_mode(self):
        self._is_AI = True

    def reset(self):
        self._hostages_count = 0
        self.last_move = (-1, -1)

    def __str__(self):
        stone_name = str(self.stone_type)
        if 'Black' in stone_name:
            return 'черный'
        elif 'White' in stone_name:
            return 'белый'
