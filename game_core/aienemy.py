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
        neighbors = self._interior_game.game_field. \
            get_neighbor_count_on_position(point.x, point.y, self._player)

        attractiveness += neighbors[0] * 2
        attractiveness += neighbors[1]

        try:
            self._interior_game.make_move('move', point.x + 1, point.y + 1)
        except IncorrectMove:
            return 0

        score = self._interior_game.get_result()
        player_name = 'Белый' if str(self._player) == 'белый' else 'Черный'
        player_score = score[player_name]

        return attractiveness + player_score

    def get_best_move(self) -> Point:
        with Pool(processes=self._interior_game.field_size) as pool:
            ans = pool.map(self.get_cell_attractiveness, self.points_set)

        best_point = self.points_set[random.randint(0, len(self.points_set))]
        best_score = 0

        for index, point_score in enumerate(ans):
            if point_score > best_score:
                best_score = point_score
                best_point = self.points_set[index]

        return best_point

    def make_move(self, game):
        if game.is_field_filled:
            game.make_move('pass')

        self._copy_game(game)
        best_move_point = self.get_best_move()

        x_move = best_move_point.x
        y_move = best_move_point.y
        while True:
            try:
                game.make_move('move', x_move + 1, y_move + 1)
                break
            except IncorrectMove:
                x_move = random.randint(0, game.field_size)
                y_move = random.randint(0, game.field_size)
