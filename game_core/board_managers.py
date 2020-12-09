from abc import abstractmethod
import re


class BoardManager:
    @abstractmethod
    def get_board_name(self):
        """Имя"""

    @abstractmethod
    def get_board_str(self) -> str:
        """Текс таблицы"""


class ScoreBoardManager(BoardManager):
    def __init__(self, score_file_name: str):
        self.is_debug = False
        self._file_name = score_file_name
        self.score_table = dict()
        self._read_board()

    def get_board_name(self):
        return 'Таблица рейтинга'

    def get_board_str(self) -> str:
        with open(self._file_name, 'r') as file:
            data = file.read()

        return data

    def _read_board(self):
        with open(self._file_name, 'r') as file:
            data = file.read()

        lines = data.split('\n')

        for line in lines:
            data = re.findall(r'(\w+)', line)
            if not data:
                break
            pos, name, score = int(data[0]), data[1], int(data[2])
            self.score_table[name] = score

    def set_player_score(self, player_name: str, score: int):
        if player_name in self.score_table:
            self.score_table[player_name] = self.score_table[player_name] + score
        else:
            self.score_table[player_name] = score

        self._write_in_file()

    def _write_in_file(self):
        lines = list()
        i = 1
        for name, score in sorted(self.score_table.items(),
                                  key=lambda _t: _t[1],
                                  reverse=True):
            pos_str = f'{i}'.ljust(8, ' ')
            name_str = f'{name}'.ljust(12, ' ')
            score_str = f'{score}'.ljust(9, ' ')

            line_str = f'{pos_str}{" " * 40}{name_str}{" " * 25}{score_str}\n'
            lines.append(line_str)
            i += 1

        with open(self._file_name, 'w') as file:
            if not self.is_debug:
                file.writelines(lines)


class LogBoardManager(BoardManager):
    def __init__(self):
        self.logs = list()

    def get_board_str(self) -> str:
        return '\n'.join(self.logs)

    def get_board_name(self):
        return 'История действий'

    def set_log(self, log: str, player: str):
        self.logs.append(f'{player}: {log}')
