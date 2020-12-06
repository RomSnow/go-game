"""Модуль для управления игровым процессом"""
from itertools import cycle
from queue import Queue

import game_core.field as field
import game_core.player as player
import game_core.stones as stones
import game_core.special_exceptions as exc
import game_core.aienemy as ai
from game_core.game_modes import GameModes
from game_core.game_params import GameParams
from web.connect_service import ConnectionService
from web.flag import Flag
from web.web_exceptions import WrongConnection


class Game:
    def __init__(self, field_params: field.FieldParams,
                 white_player: player.Player,
                 black_player: player.Player,
                 main_player: str,
                 is_ai_mode=False,
                 connect_service: ConnectionService = None
                 ):

        self._white_pl = white_player
        self._back_pl = black_player
        self._field = field.GameField(field_params)
        self._players = cycle([white_player, black_player])
        self._game_is_on = True
        self._is_ai_mode = False
        self.is_online_mode = bool(connect_service)
        self._current_player = next(self._players)
        self._is_pass = False
        self._connect_service = connect_service

        if is_ai_mode:
            if main_player == 'white':
                enemy = black_player
            else:
                enemy = white_player

            self._init_ai(enemy)

            if self.current_player == enemy:
                self.make_ai_move()

    """Класс, хранящий все данные текущей игры и управляющий ее ходом"""

    @property
    def game_is_on(self):
        return self._game_is_on

    @property
    def is_field_filled(self):
        return self._field.is_filled

    @property
    def current_player(self):
        return self._current_player

    @property
    def field_size(self):
        return self._field.field_params.column_count

    @property
    def game_field(self):
        return self._field

    def get_stone_on_position(self, x, y) -> stones.Stone:
        return self._field.get_obj_on_position(x - 1, y - 1)

    def make_move(self, move: str, x=-1, y=-1, is_ai_move=False):
        self._make_move(move, x, y, is_ai_move)
        if self._connect_service:
            self._connect_service.send_move(move, field.Point(x, y))

    def wait_online_move(self, queue: Queue, exit_flag: Flag):
        try:
            answer = self._connect_service.wait_move(exit_flag)
        except SystemExit:
            exit_flag.is_up = False
            queue.put(0)
            return
        except WrongConnection:
            queue.put(2)
            exit_flag.is_up = False
            return

        data = answer.split()
        if not data or data[0] == 'exit':
            queue.put(1)
            exit_flag.is_up = False
            return
        self._make_move(data[0], int(data[1]), int(data[2]))
        queue.put(0)
        exit_flag.is_up = False

    def _make_move(self, move: str, x=-1, y=-1, is_ai_move=False):
        """Проделывает ход, соответсвующий параметру move

            move == move - ставит фишку игрока на позицию x, y;
            move == pass - пассующий ход
        """

        if move == 'move':
            self._field.set_stone_on_position(self.current_player,
                                              x - 1, y - 1)
            self._is_pass = False

            if self._field.is_filled:
                self._game_is_on = False

        elif move == 'pass':
            if self._is_pass:
                self._game_is_on = False
                return
            self._is_pass = True

        else:
            raise exc.IncorrectMove

        self._switch_player()

        if self._is_ai_mode and not is_ai_move:
            self.make_ai_move()

    def make_ai_move(self):
        self._ai.make_move(self)

    def time_limit(self, game_window):
        self._switch_player()
        if self.is_online_mode:
            if game_window.is_waiting:
                game_window.is_waiting.is_up = False
            else:
                game_window.wait_move()

        elif self._is_ai_mode:
            self.make_ai_move()

    def print_field(self):
        print(self._field)

    def get_point_count(self, current_player: player.Player):
        """Возвращет количество очков игрока"""
        points = 0
        points += current_player.hostages_count
        points += self._define_territory(current_player)

        return points

    def _define_territory(self, current_player: player.Player):
        """Высчитывает количество территории, принадлежащей игроку"""

        stone = current_player.stone_type
        territory_count = 0
        for line in range(self._field.field_params.lines_count):
            for col in range(self._field.field_params.column_count):
                if isinstance(self._field.get_obj_on_position(col, line),
                              stones.Stone):
                    continue
                if self._breadth_first_search(list(), stone,
                                              field.Point(line, col),
                                              self._field, True):
                    territory_count += 1

        return territory_count

    def _breadth_first_search(self, visited_points, stone_type,
                              point: field.Point,
                              board: field.GameField, is_last_good):
        """Проверка на принадлежность точки к територри камня"""

        if point in visited_points:
            return is_last_good

        current_obj = board.get_obj_on_position(point.y, point.x)

        new_is_last_good = is_last_good
        if (isinstance(current_obj, stone_type) or
                isinstance(current_obj, field.OutsideStone)):
            return True
        elif current_obj is not None:
            return False

        visited_points.append(point)

        return self._do_disperse(visited_points, stone_type,
                                 point, board, new_is_last_good)

    def _do_disperse(self, visited_points, stone_type,
                     point: field.Point, board, new_is_last_good):
        for delta_x, delta_y in (-1, 0), (1, 0), (0, 1), (0, -1):
            new_point = field.Point(point.x + delta_x, point.y + delta_y)
            if not self._breadth_first_search(visited_points, stone_type,
                                              new_point, board,
                                              new_is_last_good):
                return False

        return True

    def _switch_player(self):
        self._current_player = next(self._players)

    def _init_ai(self, ai_player: player.Player):
        self._ai = ai.AIEnemy(ai_player, self)
        ai_player.set_ai_mode()
        self._is_ai_mode = True

    def get_result(self) -> dict:
        white_point = self.get_point_count(self._white_pl)
        black_point = self.get_point_count(self._back_pl)
        return {'Черный': black_point,
                'Белый': white_point,
                'Победитель':
                    'Белый' if white_point > black_point else 'Черный'}


def create_game(game_params: GameParams,
                connection_service: ConnectionService = None) -> Game:
    is_ai_mode = False
    is_white_ai = False
    is_black_ai = False
    if game_params.game_mode == GameModes.ai:
        is_ai_mode = True
        if game_params.main_player == 'white':
            is_black_ai = True
        else:
            is_white_ai = True

    white_player = player.Player(stones.WhiteStone, is_white_ai)
    black_player = player.Player(stones.BlackStone, is_black_ai)

    return Game(game_params.field_params,
                white_player, black_player, game_params.main_player,
                is_ai_mode, connection_service)


class ExitException(Exception):
    pass
