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
            return self._field[y][x]
        except IndexError:
            return 1

    def set_stone_on_position(self, stone, x, y):
        if self._field[y][x]:
            raise exc.IncorrectMove

        self._field[y][x] = stone

    def remove_stone_on_position(self, x, y):
        self._field[y][x] = 0
