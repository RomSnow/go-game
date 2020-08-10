"""Классы специальных исключений"""


class IncorrectMove(Exception):
    """Исключение при неверном ходе игрока"""


class SuicideMove(IncorrectMove):
    """Самоубийственный ход"""


class BusyPoint(IncorrectMove):
    """Ход в занятую точку"""


class KOException(IncorrectMove):
    """Нарушение правила Ко"""
