from datetime import datetime


class Zodiac:
    def __init__(self, birthdate: datetime):
        self.birthdate = birthdate
        self.zodiacs = [
            "Koç",
            "Boğa",
            "İkizler",
            "Yengeç",
            "Aslan",
            "Başak",
            "Terazi",
            "Akrep",
            "Yay",
            "Oğlak",
            "Kova",
            "Balık",
        ]
        self.sign = self.find_zodiac(self.birthdate)

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

    def __str__(self):
        return self.sign
