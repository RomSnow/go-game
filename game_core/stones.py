"""Классы игровых камней"""
from game_core.field import GameField


class _Stone:
    """Родительсий класс камней"""

    def __init__(self, field: GameField, x: int, y: int):
        self.x = x
        self.y = y
        self.neighbors = set()
        self.breaths = 4

    def set_influence(self, field: GameField):
        """Подсчет и настройка влияния соседей"""
        for i, j in (0, 1), (1, 0), (0, -1), (-1, 0):
            neighbor = field.get_obj_on_position(self.x + i, self.y + j)
            if not neighbor:
                continue
            self.breaths -= 1
            if isinstance(neighbor, _Stone):
                neighbor.close_breath()

                if type(neighbor) is type(self):
                    self.neighbors.add(neighbor)
                    self.neighbors.update(neighbor.neighbors)

        for neighbor in self.neighbors:
            neighbor.add_neighbor(self)

        for rand_neigh in self.neighbors:
            self.breaths = rand_neigh.breaths
            break

    def close_breath(self):
        self.breaths -= 1
        for neighbor in self.neighbors:
            neighbor.breaths -= 1

    def add_neighbor(self, neighbor):
        self.breaths += neighbor.breaths
        self.neighbors.add(neighbor)

    def rm(self):
        pass


class WhiteStone(_Stone):
    """Класс белого камня"""


class BlackStone(_Stone):
    """Класс черного камня"""
