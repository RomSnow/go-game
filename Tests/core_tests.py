import unittest

import game_core.field as fld
import game_core.stones as stones
import game_core.special_exceptions as sp_exc


class CoreTestCase(unittest.TestCase):
    def test_move_with_stone(self):
        """Тестирование основных функий взаимодействия с полем"""
        field = fld.GameField(fld.FieldParams(3, 3, 0))

        # тест на позиционирование
        stone = field.set_stone_on_position(stones.BlackStone, 0, 0)
        self.assertEqual(field._field, [
            [stone, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ])

        # тест на невозможность повтороного позиционирования
        self.assertRaises(
            sp_exc.IncorrectMove,
            field.set_stone_on_position, stones.BlackStone, 0, 0)

        # тест на обращение
        self.assertEqual(field.get_obj_on_position(0, 0), stone)
        self.assertEqual(field.get_obj_on_position(5, 5), 1)

    def test_stone_group(self):
        field = fld.GameField(fld.FieldParams(3, 3, 0))
        first_stone = field.set_stone_on_position(stones.BlackStone, 0, 1)

        second_stone = field.set_stone_on_position(stones.BlackStone, 0, 2)

        self.assertTrue(first_stone.breaths == second_stone.breaths == 3)

        third_stone = field.set_stone_on_position(stones.BlackStone, 0, 0)

        self.assertTrue(first_stone.breaths ==
                        second_stone.breaths ==
                        third_stone.breaths == 3)

        fourth_stone = field.set_stone_on_position(stones.BlackStone, 1, 1)

        self.assertTrue(first_stone.breaths ==
                        second_stone.breaths ==
                        third_stone.breaths ==
                        fourth_stone.breaths == 5)

    def test_close_group_breath(self):
        field = fld.GameField(fld.FieldParams(3, 3, 0))
        first_stone = field.set_stone_on_position(stones.BlackStone, 0, 1)
        second_stone = field.set_stone_on_position(stones.BlackStone, 0, 2)
        third_stone = field.set_stone_on_position(stones.BlackStone, 0, 0)
        fourth_stone = field.set_stone_on_position(stones.BlackStone, 1, 1)

        enemy_stone = field.set_stone_on_position(stones.WhiteStone, 1, 0)
        self.assertTrue(first_stone.breaths ==
                        second_stone.breaths ==
                        third_stone.breaths ==
                        fourth_stone.breaths == 3)

        self.assertEqual(enemy_stone.breaths, 1)


if __name__ == '__main__':
    unittest.main()
