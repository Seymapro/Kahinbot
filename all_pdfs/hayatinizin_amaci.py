import os

dogum_tarihi = input(
    "Arada boşluk olmadan, tamamen sayılarla tam doğum tarihini gir (0'lar önemli değil): "
)
toplam = 0
for num in dogum_tarihi:
    toplam += int(num)
ilk_toplam = toplam

if toplam > 9:
    toplam = sum(int(num) for num in str(toplam))
son_toplam = toplam

hayat_sayisi = f"{ilk_toplam}_{son_toplam}"

# print(hayat_sayisi)

file_name = f"{hayat_sayisi}.md"
relative_path = os.path.join(file_name)
with open(relative_path, "r", encoding="utf-8") as numara_file:
    print(numara_file.read())
