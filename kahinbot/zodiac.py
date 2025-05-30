# MIT License
#
# Copyright (c) 2024 Şeyma Yardım
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from datetime import datetime
from pathlib import Path


class Zodiac:
    def __init__(self, birthdate: datetime):
        self.birthdate = birthdate
        self.zodiacs = [
            ("Koç", 8),
            ("Boğa", 9),
            ("İkizler", 7),
            ("Yengeç", 2),
            ("Aslan", 3),
            ("Başak", 1),
            ("Terazi", 9),
            ("Akrep", 8),
            ("Yay", 7),
            ("Oğlak", 6),
            ("Kova", 5),
            ("Balık", 4),
        ]

        self.sign, self.enneagram = self.find_zodiac(self.birthdate)

    def find_zodiac(self, birthdate: datetime):
        day = birthdate.day
        month = birthdate.month

        if (month == 3 and day >= 21) or (month == 4 and day <= 20):
            return self.zodiacs[0]  # Koç
        elif (month == 4 and day >= 21) or (month == 5 and day <= 21):
            return self.zodiacs[1]  # Boğa
        elif (month == 5 and day >= 22) or (month == 6 and day <= 21):
            return self.zodiacs[2]  # İkizler
        elif (month == 6 and day >= 22) or (month == 7 and day <= 22):
            return self.zodiacs[3]  # Yengeç
        elif (month == 7 and day >= 23) or (month == 8 and day <= 23):
            return self.zodiacs[4]  # Aslan
        elif (month == 8 and day >= 24) or (month == 9 and day <= 23):
            return self.zodiacs[5]  # Başak
        elif (month == 9 and day >= 24) or (month == 10 and day <= 23):
            return self.zodiacs[6]  # Terazi
        elif (month == 10 and day >= 24) or (month == 11 and day <= 22):
            return self.zodiacs[7]  # Akrep
        elif (month == 11 and day >= 23) or (month == 12 and day <= 21):
            return self.zodiacs[8]  # Yay
        elif (month == 12 and day >= 22) or (month == 1 and day <= 20):
            return self.zodiacs[9]  # Oğlak
        elif (month == 1 and day >= 21) or (month == 2 and day <= 19):
            return self.zodiacs[10]  # Kova
        elif (month == 2 and day >= 20) or (month == 3 and day <= 20):
            return self.zodiacs[11]  # Balık
        else:
            raise Exception("Invalid date")

    def zodiac_to_contents(self, content_dir: Path) -> list[str]:
        contents: list[str] = []
        pin = self.enneagram

        with open(content_dir / f"tip{pin}.md", "r", encoding="UTF-8") as f:
            contents.append(f.read().strip())

        return "\n".join(contents)

    def __str__(self):
        return f"Burç: {self.sign} \nEnneagram: {self.enneagram}\nİçerik: {self.zodiac_to_contents(Path('/home/nigella/tg_bot/kahin-bot/kahinbot/enneagram'))}"
