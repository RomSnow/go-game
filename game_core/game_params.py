from dataclasses import dataclass

from game_core.field import FieldParams
from game_core.game_modes import GameModes


@dataclass
class GameParams:
    game_mode: GameModes
    field_params: FieldParams
    is_time_mode: bool
    main_player: str = 'white'
