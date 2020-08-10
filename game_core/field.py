"""Модуль для работы с игровым полем"""

import game_core.special_exceptions as exc
import game_core.player as player


class FieldParams:
    """Хранит параметры для поля"""

    def __init__(
            self, lines_count, column_count
    ):
        self.lines_count = lines_count
        self.column_count = column_count


class GameField:
    """Содержит все данные и функции игрового поля"""

    def __init__(self, params: FieldParams):
        self._params = params
        self._field = [
            [
                0 for col in range(params.column_count)
            ]
            for lin in range(params.lines_count)
        ]

    def get_obj_on_position(self, x, y):
        try:
            if y < 0 or x < 0:
                raise IndexError
            return self._field[y][x]
        except IndexError:
            return 1

    def set_stone_on_position(self, master: player.Player, x: int, y: int):
        if self._field[y][x]:
            raise exc.IncorrectMove

        stone = master.stone_type(x, y, master)
        self._field[y][x] = stone
        stone.set_influence(self)
        return stone

    def remove_stone_on_position(self, x, y):
        self._field[y][x] = 0

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
