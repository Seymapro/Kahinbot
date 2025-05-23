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
            ("Başak", (1, 6)),
            ("Terazi", 9),
            ("Akrep", 8),
            ("Yay", 7),
            ("Oğlak", (6, 1)),
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
        if isinstance(pin, int):
            with open(content_dir / f"tip{pin}.md", "r", encoding="UTF-8") as f:
                contents.append(f.read().strip())
        else: 
            for i in pin:
                with open(content_dir / f"tip{i}.md", "r", encoding="UTF-8") as f:
                    contents.append(f.read().strip())

        return contents


    def __str__(self):
        return f"Burç: {self.sign} \nEnneagram: {self.enneagram}\nİçerik: {self.zodiac_to_contents(Path('./enneagram/'))}"


"""
Koç – Mars: 8

Boğa – Venüs: 9

İkizler – Merkür: 7

Yengeç – Ay: 2

Aslan – Güneş: 3

Başak – Merkür: 1, 6

Terazi – Venüs: 9

Akrep – Plüton, Mars: 8

Yay – Jüpiter: 7

Oğlak – Satürn: 6, 1

Kova – Uranüs: 5

Balık – Neptün: 4
"""
