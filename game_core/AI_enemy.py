import random

import game_core.game_manager as gm


class AI_enemy:
    """Класс с реализацией компьютерного противника"""

    def __init__(self, player: gm.player.Player):
        self._player = player

    @property
    def player(self):
        return self._player

    @staticmethod
    def make_move(game: gm.Game):
        size = game.field_size
        move_coordinates = (random.randint(1, size),
                            random.randint(1, size))

        if game.is_field_filled:
            game.make_move('pass')

        no_completed = False
        while no_completed:
            try:
                game.make_move('move', *move_coordinates)
            except Exception:
                continue

            no_completed = True
