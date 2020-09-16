"""Модуль для управления игровым процессом"""
from itertools import cycle

import game_core.field as field
import game_core.player as player
import game_core.stones as stones
import game_core.special_exceptions as exc


class Game:
    """Класс, хранящий все данные текущей игры и управляющий ее ходом"""

    def __init__(self, field_params: field.FieldParams,
                 first_player: player.Player,
                 second_player: player.Player):

        self._field = field.GameField(field_params)
        self._players = cycle([first_player, second_player])
        self._game_is_on = True
        self._current_player = next(self._players)
        self._is_pass = False

    @property
    def game_is_on(self):
        return self._game_is_on

    @property
    def current_player(self):
        return self._current_player

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
                              stones._Stone):
                    continue
                if self._breadth_first_search(list(), stone, (line, col),
                                              self._field, True):
                    territory_count += 1

        return territory_count

    def _breadth_first_search(self, visited_points: list, stone_type,
                              point, board: field.GameField, is_last_good):
        """Проверка на принадлежность точки к територри камня"""

        if point in visited_points:
            return is_last_good

        current_obj = board.get_obj_on_position(point[1], point[0])

        new_is_last_good = is_last_good
        if isinstance(current_obj, stone_type) or current_obj == 1:
            return True
        elif current_obj == 0:
            pass
        else:
            return False

        visited_points.append(point)

        return (self._breadth_first_search(visited_points, stone_type,
                                           (point[0] + 1, point[1]),
                                           board, new_is_last_good) and
                self._breadth_first_search(visited_points, stone_type,
                                           (point[0] - 1, point[1]),
                                           board, new_is_last_good) and
                self._breadth_first_search(visited_points, stone_type,
                                           (point[0], point[1] + 1),
                                           board, new_is_last_good) and
                self._breadth_first_search(visited_points, stone_type,
                                           (point[0], point[1] - 1),
                                           board, new_is_last_good)
                )

    def _switch_player(self):
        self._current_player = next(self._players)
