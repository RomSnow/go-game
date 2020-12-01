from dataclasses import dataclass

from game_core.field import FieldParams
from game_core.game_modes import GameModes


@dataclass
class GameParams:
    game_mode: GameModes
    field_params: FieldParams
    is_time_mode: bool
    second_on_move: int = 5
    main_player: str = 'white'

    def __str__(self):
        return f'{self.game_mode},{self.field_params.column_count},' \
               f'{self.is_time_mode},' \
               f'{"white" if self.main_player == "black" else "black"},' \
               f'{self.second_on_move}'
