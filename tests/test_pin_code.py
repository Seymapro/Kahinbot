from datetime import datetime
from kahinbot.pin_code import get_pin_code

import unittest


class PinCodeInputTestCase(unittest.TestCase):
    def test_not_datetime(self) -> None:
        self.assertRaises(AttributeError, get_pin_code, "31.07.2002")

    def test_datetime(self) -> None:
        self.assertIsInstance(get_pin_code(datetime(2002, 7, 31)), list)


class PinCodeCalculationTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.pin_code_map = {
            datetime(2002, 7, 31): [4, 7, 4, 6, 1, 2, 2, 4, 3],
            datetime(2002, 12, 22): [4, 3, 4, 2, 6, 7, 7, 5, 2],
        }

    def test_pin_code(self) -> None:
        for birthdate, pin_code in self.pin_code_map.items():
            with self.subTest(birthdate=birthdate, pin_code=pin_code):
                self.assertListEqual(pin_code, get_pin_code(birthdate))
