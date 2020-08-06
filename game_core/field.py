"""Модуль для работы с игровым полем"""

import game_core.special_exceptions as exc


class FieldParams:
    """Хранит параметры для поля"""

    def __init__(
            self, lines_count, column_count, game_difficult
    ):
        self.lines_count = lines_count
        self.column_count = column_count
        self.game_difficult = game_difficult


class GameField:
    """Содержит все данные и функции игрового поля"""

    def __init__(self, params: FieldParams):
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

    def set_stone_on_position(self, stone_type, x, y):
        if self._field[y][x]:
            raise exc.IncorrectMove

        stone = stone_type(self, x, y)
        self._field[y][x] = stone
        stone.set_influence(self)
        return stone

    def remove_stone_on_position(self, x, y):
        self._field[y][x].rm()
        self._field[y][x] = 0
