import random
import copy
from multiprocessing import Process, Pool

from game_core.special_exceptions import IncorrectMove
from game_core.field import Point


class AIEnemy:
    """Класс с реализацией компьютерного противника"""

    def __init__(self, player, game=None):
        self._player = player
        self._interior_game = game
        self.points_set = [Point(x, y) for x in range(game.field_size)
                           for y in range(game.field_size)]

    @property
    def player(self):
        return self._player

    def _copy_game(self, game):
        self._interior_game = copy.deepcopy(game)

    def get_cell_attractiveness(self, point: Point) -> int:
        attractiveness = 0
        if not self._interior_game.game_field\
                .get_obj_on_position(point.x, point.y):
            for neighbor in self._interior_game.\
                    game_field.get_neighbor_on_position(point):
                if neighbor.breaths == 1:
                    attractiveness += 200
                attractiveness += 100 - neighbor.breaths * 5

        return attractiveness

    def get_best_move(self) -> Point:
        results = list()
        for point in self.points_set:
            results.append(self.get_cell_attractiveness(point))

        best_point = self.points_set[
            random.randint(0, len(self.points_set) - 1)]
        best_score = 0

        for index, point_score in enumerate(results):
            if point_score > best_score:
                best_score = point_score
                best_point = self.points_set[index]

        return best_point

    def make_move(self, game):
        if game.is_field_filled:
            game.make_move('pass', True)

        best_move_point = self.get_best_move()

        x_move = best_move_point.x
        y_move = best_move_point.y
        while True:
            try:
                game.make_move('move', x_move + 1, y_move + 1, True)
                break
            except IncorrectMove:
                x_move = random.randint(0, game.field_size)
                y_move = random.randint(0, game.field_size)
