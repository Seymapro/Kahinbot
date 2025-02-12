from datetime import datetime
from kahinbot.zodiac import Zodiac

import unittest


class ZodiacInputTestCase(unittest.TestCase):
    def test_not_datetime(self) -> None:
        self.assertRaises(AttributeError, Zodiac, "31.07.2002")

    def test_datetime(self) -> None:
        self.assertEqual("Aslan", Zodiac(datetime(2002, 7, 31)).sign)


class ZodiacSignTestCase(unittest.TestCase):
    def test_aries(self) -> None:
        # Leonardo da Vinci
        self.assertEqual("Koç", Zodiac(datetime(1452, 4, 15)).sign)

    def test_taurus(self) -> None:
        # Pyotr Ilyich Tchaikovsky
        self.assertEqual("Boğa", Zodiac(datetime(1840, 5, 7)).sign)

    def test_gemini(self) -> None:
        # Theodore John Kaczynski
        self.assertEqual("İkizler", Zodiac(datetime(1942, 5, 22)).sign)

    def test_cancer(self) -> None:
        # Alan Mathison Turing
        self.assertEqual("Yengeç", Zodiac(datetime(1912, 6, 23)).sign)

    def test_leo(self) -> None:
        # Napoleone di Buonaparte
        self.assertEqual("Aslan", Zodiac(datetime(1769, 8, 15)).sign)

    def test_virgo(self) -> None:
        # Beyoncé Giselle Knowles-Carter
        self.assertEqual("Başak", Zodiac(datetime(1981, 9, 4)).sign)

    def test_libra(self) -> None:
        # Gwen Stefani
        self.assertEqual("Terazi", Zodiac(datetime(1969, 10, 3)).sign)

    def test_scorpio(self) -> None:
        # Marie Curie
        self.assertEqual("Akrep", Zodiac(datetime(1867, 11, 7)).sign)

    def test_sagittarius(self) -> None:
        # Billie Eilish Pirate Baird
        self.assertEqual("Yay", Zodiac(datetime(2001, 12, 18)).sign)

    def test_capricorn(self) -> None:
        # John Ronald Reuel Tolkien
        self.assertEqual("Oğlak", Zodiac(datetime(1892, 1, 3)).sign)

    def test_aquarius(self) -> None:
        # Galileo Galilei
        self.assertEqual("Kova", Zodiac(datetime(1564, 2, 15)).sign)

    def test_pisces(self) -> None:
        # Albert Einstein
        self.assertEqual("Balık", Zodiac(datetime(1879, 3, 14)).sign)
