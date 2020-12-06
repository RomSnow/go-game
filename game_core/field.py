"""Модуль для работы с игровым полем"""

from dataclasses import dataclass

import game_core.player as player
import game_core.special_exceptions as exc


class FieldParams:
    """Хранит параметры для поля"""

    def __init__(self, size):
        self.lines_count = size
        self.column_count = size


@dataclass
class Point:
    x: int
    y: int


class GameField:
    """Содержит все данные и функции игрового поля"""

    def __init__(self, params: FieldParams):
        self._params = params
        self._field = [
            [
                None for col in range(params.column_count)
            ]
            for lin in range(params.lines_count)
        ]

    @property
    def field_params(self):
        return self._params

    @property
    def is_filled(self):
        for i in self._field:
            for j in i:
                if j is None:
                    return False
        return True

    def get_obj_on_position(self, x, y):
        try:
            if y < 0 or x < 0:
                raise IndexError
            return self._field[y][x]
        except IndexError:
            return OutsideStone()

    def set_stone_on_position(self, master: player.Player, x: int, y: int):
        try:
            if self._field[y][x]:
                raise exc.BusyPoint
        except IndexError:
            raise exc.IncorrectMove

        if (x, y) == master.last_move:
            raise exc.KOException

        stone = master.stone_type(x, y, master)
        stone.set_influence(self)
        self._field[y][x] = stone
        master.last_move = (x, y)
        return stone

    def get_neighbor_on_position(self, point: Point):
        for shift_x in (-1, 0, 1):
            for shift_y in (-1, 0, 1):
                if shift_x and shift_y or shift_x == shift_y:
                    continue

                stone = self.get_obj_on_position(point.x + shift_x,
                                                 point.y + shift_y)

                if isinstance(stone, OutsideStone) or not stone:
                    continue

                yield stone

    def remove_stone_on_position(self, x: int, y: int):
        self._field[y][x] = None

    def __str__(self):
        field_str = ''

        for line in self._field:
            line_str = ''
            for col in line:
                if not col:
                    col = '.'
                line_str += f'{str(col)}-'

            field_str += line_str[:-1] + '\n'
            field_str += str(self._params.column_count * '| ')[:-1] + '\n'

        return field_str[:-(self._params.column_count * 2 + 1)] + '\n'


class OutsideStone:
    """Класс камней лежащих вне поля"""
