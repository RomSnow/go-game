"""Модуль для работы с игровым полем"""

from dataclasses import dataclass

import game_core.special_exceptions as exc
import game_core.player as player


class FieldParams:
    """Хранит параметры для поля"""

    def __init__(self, size):
        self.lines_count = size
        self.column_count = size


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

    def get_obj_on_position(self, x, y):
        try:
            if y < 0 or x < 0:
                raise IndexError
            return self._field[y][x]
        except IndexError:
            return OutsideStone()

    def set_stone_on_position(self, master: player.Player, x: int, y: int):
        if self._field[y][x]:
            raise exc.BusyPoint

        if (x, y) == master.last_move:
            raise exc.KOException

        stone = master.stone_type(x, y, master)
        stone.set_influence(self)
        self._field[y][x] = stone
        master.last_move = (x, y)
        return stone

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


@dataclass
class Point:
    x: int
    y: int
