"""Классы игровых камней"""
from game_core.field import GameField, exc, player


class Stone:
    """Родительсий класс камней"""

    def __init__(self, x: int, y: int, master: player.Player):
        self.x = x
        self.y = y
        self.friend_neighbors = set()
        self.enemy_neighbors = set()
        self.breaths = 4
        self._master = master

    def set_influence(self, field: GameField):
        """Подсчет и настройка влияния соседей"""
        # обход по соседним клеткам
        death_list = []
        for i, j in (0, 1), (1, 0), (0, -1), (-1, 0):
            neighbor = field.get_obj_on_position(self.x + i, self.y + j)

            if not neighbor:
                continue
            self.breaths -= 1

            if isinstance(neighbor, Stone):
                neighbor.close_breath()

                if type(neighbor) is type(self):
                    self.friend_neighbors.add(neighbor)
                    self.friend_neighbors.update(neighbor.friend_neighbors)
                else:
                    self.add_enemy(neighbor)
                    neighbor.add_enemy(self)
                    neighbor.check_to_death(field, death_list)

        # проверка на самоубийство
        if not self.breaths:
            try:
                neighbor = self.friend_neighbors.pop()

                if not neighbor.breaths:
                    raise exc.IncorrectMove
                self.friend_neighbors.add(neighbor)
            except KeyError:
                raise exc.SuicideMove
            except exc.IncorrectMove:
                self.friend_neighbors.add(neighbor)
                raise exc.SuicideMove

        # обновление данных группы камней
        for neighbor in self.friend_neighbors:
            neighbor.add_friend(self)

        # выравнивание дыханий текущего камня с группой
        for rand_neigh in self.friend_neighbors:
            self.breaths = rand_neigh.breaths
            break

        self._kill_enemy(field, death_list)

    def close_breath(self):
        """Закрыть дыхание у группы камней"""
        self.breaths -= 1
        for neighbor in self.friend_neighbors:
            neighbor.breaths -= 1

    def add_breath(self):
        """Добавить ранее закрытое дыхание"""
        self.breaths += 1
        for neighbor in self.friend_neighbors:
            neighbor.breaths += 1

    def add_friend(self, neighbor):
        """Добавление камня к группе"""
        self.breaths += neighbor.breaths
        self.friend_neighbors.add(neighbor)

    def add_enemy(self, enemy):
        self.enemy_neighbors.add(enemy)

    def check_to_death(self, field, death_list):
        """Проверка на состояние смерти"""
        if not self.breaths:
            death_list.append(self)

    def die(self, field: GameField) -> int:
        """Уничтожение группы камней и возвращение количества убитых"""
        neighbor_count = len(self.friend_neighbors)
        for stone in (*self.friend_neighbors, self):
            for enemy in stone.enemy_neighbors:
                enemy.add_breath()
                enemy.enemy_neighbors.remove(stone)

            field.remove_stone_on_position(stone.x, stone.y)

        return neighbor_count + 1

    def _kill_enemy(self, field, death_list):
        for stone in death_list:
            self._master.add_hostages(stone.die(field))


class WhiteStone(Stone):
    """Класс белого камня"""

    def __str__(self):
        return '*'


class BlackStone(Stone):
    """Класс черного камня"""

    def __str__(self):
        return 'o'
