import unittest

import game_core.field as fld
import game_core.stones as stones
import game_core.special_exceptions as sp_exc
import game_core.player as player


class CoreTestCase(unittest.TestCase):
    """Тестирование основных функий взаимодействия с полем"""

    def test_move_with_stone(self):
        field = fld.GameField(fld.FieldParams(3))
        master = player.Player(stones.BlackStone)
        # тест на позиционирование
        stone = field.set_stone_on_position(master, 0, 0)
        self.assertEqual(field._field, [
            [stone, None, None],
            [None, None, None],
            [None, None, None]
        ])

        # тест на невозможность повтороного позиционирования
        self.assertRaises(
            sp_exc.BusyPoint,
            field.set_stone_on_position, stones.BlackStone, 0, 0)

        # тест на обращение
        self.assertEqual(field.get_obj_on_position(0, 0), stone)
        self.assertTrue(isinstance(
            field.get_obj_on_position(5, 5), fld.OutsideStone)
        )

    def test_stone_group(self):
        field = fld.GameField(fld.FieldParams(3))
        master = player.Player(stones.BlackStone)
        first_stone = field.set_stone_on_position(master, 0, 1)

        second_stone = field.set_stone_on_position(master, 0, 2)

        self.assertTrue(first_stone.breaths == second_stone.breaths == 3)

        third_stone = field.set_stone_on_position(master, 0, 0)

        self.assertTrue(first_stone.breaths ==
                        second_stone.breaths ==
                        third_stone.breaths == 3)

        fourth_stone = field.set_stone_on_position(master, 1, 1)

        self.assertTrue(first_stone.breaths ==
                        second_stone.breaths ==
                        third_stone.breaths ==
                        fourth_stone.breaths == 5)

    def test_close_group_breath(self):
        field = fld.GameField(fld.FieldParams(3))
        master = player.Player(stones.BlackStone)
        enemy_master = player.Player(stones.WhiteStone)

        first_stone = field.set_stone_on_position(master, 0, 1)
        second_stone = field.set_stone_on_position(master, 0, 2)
        third_stone = field.set_stone_on_position(master, 0, 0)
        fourth_stone = field.set_stone_on_position(master, 1, 1)

        enemy_stone = field.set_stone_on_position(enemy_master, 1, 0)
        self.assertTrue(first_stone.breaths ==
                        second_stone.breaths ==
                        third_stone.breaths ==
                        fourth_stone.breaths == 3)

        self.assertEqual(enemy_stone.breaths, 1)

    def test_suicide_move(self):
        field = fld.GameField(fld.FieldParams(3))
        master = player.Player(stones.BlackStone)
        enemy_master = player.Player(stones.WhiteStone)

        field.set_stone_on_position(master, 1, 0)
        field.set_stone_on_position(master, 1, 1)
        field.set_stone_on_position(master, 0, 2)

        field.set_stone_on_position(enemy_master, 0, 0)

        self.assertRaises(sp_exc.SuicideMove,
                          field.set_stone_on_position, enemy_master, 0, 1)

    def test_stone_death(self):
        field = fld.GameField(fld.FieldParams(3))
        black_master = player.Player(stones.BlackStone)
        white_master = player.Player(stones.WhiteStone)

        field.set_stone_on_position(black_master, 0, 0)
        white_stone_1 = field.set_stone_on_position(white_master, 0, 1)
        white_stone_2 = field.set_stone_on_position(white_master, 1, 1)
        white_stone_3 = field.set_stone_on_position(white_master, 1, 0)

        self.assertEqual(field.get_obj_on_position(0, 0), None)
        self.assertEqual(white_stone_1.breaths, 6)
        self.assertEqual(white_stone_2.breaths, 6)
        self.assertEqual(white_stone_3.breaths, 6)

        self.assertEqual(white_master._hostages_count, 1)

    def test_group_death(self):
        field = fld.GameField(fld.FieldParams(3))
        black_master = player.Player(stones.BlackStone)
        white_master = player.Player(stones.WhiteStone)

        field.set_stone_on_position(black_master, 0, 0)
        field.set_stone_on_position(black_master, 0, 1)

        white_stone_1 = field.set_stone_on_position(white_master, 1, 0)
        white_stone_2 = field.set_stone_on_position(white_master, 1, 1)
        white_stone_3 = field.set_stone_on_position(white_master, 1, 2)
        white_stone_4 = field.set_stone_on_position(white_master, 0, 2)

        self.assertEqual(field.get_obj_on_position(0, 0), None)
        self.assertEqual(field.get_obj_on_position(0, 1), None)

        self.assertTrue(white_stone_1.breaths ==
                        white_stone_2.breaths ==
                        white_stone_3.breaths ==
                        white_stone_4.breaths == 6)

        self.assertEqual(white_master._hostages_count, 2)

    def test_field_str(self):
        field = fld.GameField(fld.FieldParams(6))

        self.assertEqual(str(field), ('.-.-.-.-.-.\n' +
                                      '| | | | | |\n' +
                                      '.-.-.-.-.-.\n' +
                                      '| | | | | |\n' +
                                      '.-.-.-.-.-.\n' +
                                      '| | | | | |\n' +
                                      '.-.-.-.-.-.\n' +
                                      '| | | | | |\n' +
                                      '.-.-.-.-.-.\n' +
                                      '| | | | | |\n' +
                                      '.-.-.-.-.-.\n')
                         )

        field.set_stone_on_position(player.Player(stones.BlackStone), 3, 3)

        self.assertEqual(str(field), ('.-.-.-.-.-.\n' +
                                      '| | | | | |\n' +
                                      '.-.-.-.-.-.\n' +
                                      '| | | | | |\n' +
                                      '.-.-.-.-.-.\n' +
                                      '| | | | | |\n' +
                                      '.-.-.-o-.-.\n' +
                                      '| | | | | |\n' +
                                      '.-.-.-.-.-.\n' +
                                      '| | | | | |\n' +
                                      '.-.-.-.-.-.\n')
                         )

    def test_ko(self):
        field = fld.GameField(fld.FieldParams(3))
        black_master = player.Player(stones.BlackStone)
        white_master = player.Player(stones.WhiteStone)

        stone = field.set_stone_on_position(black_master, 1, 0)

        stone.die(field)

        self.assertRaises(sp_exc.KOException, field.set_stone_on_position,
                          black_master, 1, 0)


if __name__ == '__main__':
    unittest.main()
