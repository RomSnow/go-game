import copy
import random
from typing import List

from game_core.field import Point, OutsideStone
from game_core.special_exceptions import IncorrectMove


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
            is_have_exit = False
            is_all_friend = True
            is_one_breath = False
            for neighbor in self._interior_game. \
                    game_field.get_neighbor_on_position(point):
                if isinstance(neighbor, self._player.stone_type):
                    if neighbor.breaths == 1:
                        is_one_breath = True
                        attractiveness += 100
                    attractiveness += 100 - neighbor.breaths * 2
                elif isinstance(neighbor, OutsideStone):
                    pass
                elif neighbor is None:
                    is_have_exit = True
                else:
                    is_all_friend = False
                    if neighbor.breaths == 1:
                        attractiveness += 100
                    attractiveness += 100 - neighbor.breaths * 2

            if is_all_friend or (is_one_breath and not is_have_exit):
                attractiveness = 0

        return attractiveness

    def get_best_move(self) -> List[Point]:
        results = list()
        for point in self.points_set:
            results.append(self.get_cell_attractiveness(point))

        best_point = self.points_set[
            random.randint(0, len(self.points_set) - 1)]
        best_score = 0
        best_points = [best_point]
        for index, point_score in enumerate(results):
            if point_score > best_score:
                best_score = point_score
                best_points = [self.points_set[index]]
            elif point_score == best_score:
                best_points.append(self.points_set[index])
        return best_points

    def make_move(self, game):
        if game.is_field_filled:
            game.make_move('pass', True)

        best_move_points = self.get_best_move()
        points_iter = iter(best_move_points)

        move_point = next(points_iter)
        x_move = move_point.x
        y_move = move_point.y
        while True:
            try:
                game.make_move('move', x_move + 1, y_move + 1, True)
                break
            except IncorrectMove:
                try:
                    move_point = next(points_iter)
                    x_move = move_point.x
                    y_move = move_point.y
                except StopIteration:
                    x_move = random.randint(0, game.field_size)
                    y_move = random.randint(0, game.field_size)
