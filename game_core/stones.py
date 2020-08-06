"""Классы игровых камней"""
from game_core.field import GameField


class _Stone:
    """Родительсий класс камней"""

    def __init__(self, field: GameField, x: int, y: int):
        self.x = x
        self.y = y
        self.neighbors = []
        self.breaths = 4
        self._set_influence(field)

    def _set_influence(self, field: GameField):
        """Подсчет и настройка влияния соседей"""
        for i, j in (0, 1), (1, 0), (0, -1), (-1, 0):
            neighbor = field.get_obj_on_position(self.x + i, self.y + j)
            if not neighbor:
                continue
            self.breaths -= 1
            if neighbor is _Stone:
                neighbor.close_breath()

                if neighbor is type(self):
                    self.neighbors.append(neighbor)

        for neighbor in self.neighbors:
            neighbor.add_neighbor(self)

        self.breaths = self.neighbors[0].breaths

    def close_breath(self):
        self.breaths -= 1
        for neighbor in self.neighbors:
            neighbor.breaths -= 1

    def add_neighbor(self, neighbor):
        self.breaths += neighbor.breaths


class WhiteStone(_Stone):
    """Класс белого камня"""


class BlackStone(_Stone):
    """Класс черного камня"""
