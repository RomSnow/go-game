import random


class Ai_enemy:
    """Класс с реализацией компьютерного противника"""

    def __init__(self, player):
        self._player = player

    @property
    def player(self):
        return self._player

    @staticmethod
    def make_move(game):
        size = game.field_size

        if game.is_field_filled:
            game.make_move('pass')

        no_completed = True
        while no_completed:
            move_coordinates = (random.randint(1, size),
                                random.randint(1, size))
            try:
                game.make_move('move', *move_coordinates, True)
            except Exception:
                continue

            no_completed = False
