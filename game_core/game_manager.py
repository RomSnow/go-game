"""Модуль для управления игровым процессом"""
from itertools import cycle

import game_core.field as field
import game_core.player as player
import game_core.stones as stones
import game_core.special_exceptions as exc
import game_core.ai_enemy as ai


class Game:
    """Класс, хранящий все данные текущей игры и управляющий ее ходом"""

    def __init__(self, field_params: field.FieldParams,
                 first_player: player.Player,
                 second_player: player.Player,
                 is_ai_mode=False):

        self._field = field.GameField(field_params)
        self._players = cycle([first_player, second_player])
        self._game_is_on = True
        self._is_ai_mode = False
        self._current_player = next(self._players)
        self._is_pass = False

        if is_ai_mode:
            self._init_ai(second_player)

    @property
    def game_is_on(self):
        return self._game_is_on

    @property
    def is_field_filled(self):
        return self._field.is_filled

    @property
    def current_player(self):
        return self._current_player

    @property
    def field_size(self):
        return self._field.field_params.column_count

    def get_stone_on_position(self, x, y) -> stones.Stone:
        return self._field.get_obj_on_position(x - 1, y - 1)

    def make_move(self, move: str, x=-1, y=-1):
        """Проделывает ход, соответсвующий параметру move

            move == move - ставит фишку игрока на позицию x, y;
            move == pass - пассующий ход
        """
        if move == 'move':
            self._field.set_stone_on_position(self.current_player,
                                              x - 1, y - 1)
            self._is_pass = False

        elif move == 'pass':
            if self._is_pass:
                self._game_is_on = False
                return
            self._is_pass = True

        else:
            raise exc.IncorrectMove

        self._switch_player()

    def make_ai_move(self):
        self._ai.make_move(self)

    def print_field(self):
        print(self._field)

    def get_point_count(self, current_player: player.Player):
        """Возвращет количество очков игрока"""
        points = 0
        points += current_player.hostages_count
        points += self._define_territory(current_player)

        return points

    def _define_territory(self, current_player: player.Player):
        """Высчитывает количество территории, принадлежащей игроку"""

        stone = current_player.stone_type
        territory_count = 0
        for line in range(self._field.field_params.lines_count):
            for col in range(self._field.field_params.column_count):
                if isinstance(self._field.get_obj_on_position(col, line),
                              stones.Stone):
                    continue
                if self._breadth_first_search(list(), stone,
                                              field.Point(line, col),
                                              self._field, True):
                    territory_count += 1

        return territory_count

    def _breadth_first_search(self, visited_points, stone_type,
                              point: field.Point,
                              board: field.GameField, is_last_good):
        """Проверка на принадлежность точки к територри камня"""

        if point in visited_points:
            return is_last_good

        current_obj = board.get_obj_on_position(point.y, point.x)

        new_is_last_good = is_last_good
        if (isinstance(current_obj, stone_type) or
                isinstance(current_obj, field.OutsideStone)):
            return True
        elif current_obj is not None:
            return False

        visited_points.append(point)

        return self._do_disperse(visited_points, stone_type,
                                 point, board, new_is_last_good)

    def _do_disperse(self, visited_points, stone_type,
                     point: field.Point, board, new_is_last_good):
        for delta_x, delta_y in (-1, 0), (1, 0), (0, 1), (0, -1):
            new_point = field.Point(point.x + delta_x, point.y + delta_y)
            if not self._breadth_first_search(visited_points, stone_type,
                                              new_point, board,
                                              new_is_last_good):
                return False

        return True

    def _switch_player(self):
        self._current_player = next(self._players)

    def _init_ai(self, ai_player: player.Player):
        self._ai = ai.Ai_enemy(ai_player)
        ai_player.set_ai_mode()
        self._is_ai_mode = True
