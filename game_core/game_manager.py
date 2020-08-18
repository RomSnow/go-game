"""Модуль для управления игровым процессом"""
from itertools import cycle

import game_core.field as field
import game_core.player as player
import game_core.stones as stones
import game_core.special_exceptions as exc


class Game:
    """Класс, хранящий все данные текущей игры и управляющий ее ходом"""

    def __init__(self, field_params: field.FieldParams):
        white_player = player.Player(stones.WhiteStone)
        black_player = player.Player(stones.BlackStone)

        self._field = field.GameField(field_params)
        self._players = cycle([white_player, black_player])
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

    def _switch_player(self):
        self._current_player = next(self._players)

    def print_field(self):
        print(self._field)
