from datetime import datetime
from kahinbot.the_life import birthdate_to_life_path

import unittest


class LifePathInputTestCase(unittest.TestCase):
    def test_not_datetime(self) -> None:
        self.assertRaises(AttributeError, birthdate_to_life_path, "31.07.2002")

    def test_datetime(self) -> None:
        self.assertIsInstance(birthdate_to_life_path(datetime(2002, 7, 31)), tuple)


class LifePathCalculationTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.life_path_map = {
            datetime(2002, 7, 31): (15, 6),
            datetime(2002, 12, 22): (11, 2),
        }

    def test_life_path(self) -> None:
        for birthdate, life_path in self.life_path_map.items():
            with self.subTest(birthdate=birthdate, life_path=life_path):
                self.assertTupleEqual(life_path, birthdate_to_life_path(birthdate))
