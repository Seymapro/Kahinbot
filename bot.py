# MIT License

# Copyright (c) 2024 Seymapro

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from the_life import birthdate_to_life_path, life_path_to_content
from paraphraser import paraphrase
from telethon import TelegramClient, events, Button
from datetime import datetime
from pathlib import Path
import os
import json

__author__ = "Seymapro"
__version__ = "1.0.0"

api_id = int(os.environ["OZETCIBOT_API_ID"])
api_hash = os.environ["OZETCIBOT_API_HASH"]
bot_token = os.environ["OZETCIBOT_BOT_TOKEN"]


client = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)


@client.on(events.NewMessage(pattern="/hayatyolu"))
async def handle_lifepath_command(event):
    message_raw = event.raw_text
    try:
        birthdate = datetime.strptime(
            message_raw.split("/hayatyolu")[1].strip(), "%d.%m.%Y"
        )
    except Exception:
        await event.respond(f"Girilen mesaj ({message_raw}) hatalı!")
        return

    life_path = birthdate_to_life_path(birthdate)

    await event.respond(
        f"<b><u>HAYAT SAYISI</b></u>: {life_path[0]}/{life_path[1]}",
        buttons=[
            [Button.inline("Full Metin", f"full_text|{life_path[0]},{life_path[1]}")],
            [Button.inline("Özet", f"summary|{life_path[0]},{life_path[1]}")],
            [Button.inline("Maddeler", f"json|{life_path[0]},{life_path[1]}")],
        ],
        parse_mode="html",
    )


@client.on(events.CallbackQuery(pattern="full_text\|(.*?)"))
async def full_text(event) -> None:
    first, second = event.data.decode().split("|")[-1].split(",")
    life_path = (first, second)

    try:
        content = life_path_to_content(
            life_path, Path("/home/nigella/tg_bot/Kitap/data/millman/tr/MDs/")
        )
    except Exception as e:
        await event.respond(f"Dosya işlemlerinde hata ile karşılaşıldı: {e}")
        return

    for line in content.splitlines():
        if line.startswith("#"):
            content = content.replace(
                f"{line}\n", f"<b><u>{line.split('#')[-1].strip()}</b></u>"
            )

    message = ""
    for part in content.split("\n\n"):
        if len(message) + len(part) + 2 > 4096:
            await event.respond(message.strip(), parse_mode="html")
            message = ""
        message += f"\n\n{part}"
    else:
        await event.respond(message.strip(), parse_mode="html")


@client.on(events.CallbackQuery(pattern="json\|(.*?)"))
async def json_summ(event):
    first, second = event.data.decode().split("|")[-1].split(",")
    life_path = (first, second)

    with open(
        f"/home/nigella/tg_bot/Kitap/data/millman/tr/JSONs/{life_path[0]}_{life_path[1]}.json",
        "r",
    ) as f:
        summary_json = json.loads(f.read())

    summary_short = "<b><u>Genel Kısa Özet</b></u>\n\n"

    summary_short += f'<b><u>Temel Özellikler</b></u>\n{"".join(f"* {key_trait}{chr(10)}" for key_trait in summary_json["key_traits"])}\n\n'

    summary_short += f'<b><u>Zorluklar</b></u>\n{"".join(f"* {challenge}{chr(10)}" for challenge in summary_json["challenges"])}\n\n'

    summary_short += f'<b><u>Fırsatlar</b></u>\n{"".join(f"* {opportunity}{chr(10)}" for opportunity in summary_json["opportunities"])}\n\n'

    summary_short += f'<b><u>Sağlık</b></u>\n<b><u>Pozitif</b></u>\n{"".join(f"* {positive}{chr(10)}" for positive in summary_json["health"]["positive"])}\n<b><u>Negatif</b></u>\n{"".join(f"* {negative}{chr(10)}" for negative in summary_json["health"]["negative"])}\n<b><u>Tavsiye</b></u>\n{"".join(f"* {advice}{chr(10)}" for advice in summary_json["health"]["advice"])}\n\n'

    summary_short += f'<b><u>İlişkiler</b></u>\n<b><u>Pozitif</b></u>\n{"".join(f"* {positive}{chr(10)}" for positive in summary_json["relationships"]["positive"])}\n<b><u>Negatif</b></u>\n{"".join(f"* {negative}{chr(10)}" for negative in summary_json["relationships"]["negative"])}\n<b><u>Tavsiye</b></u>\n{"".join(f"* {advice}{chr(10)}" for advice in summary_json["relationships"]["advice"])}\n\n'

    summary_short += f'<b><u>Yetenekler, İş ve Finans</b></u>\n<b><u>Pozitif</b></u>\n{"".join(f"* {positive}{chr(10)}" for positive in summary_json["talents_work_finances"]["positive"])}\n<b><u>Negatif</b></u>\n{"".join(f"* {negative}{chr(10)}" for negative in summary_json["talents_work_finances"]["negative"])}\n<b><u>Tavsiye</b></u>\n{"".join(f"* {advice}{chr(10)}" for advice in summary_json["talents_work_finances"]["advice"])}\n\n'

    summary_short += f'<b><u>Kaderini Gerçekleştirmek</b></u>\n<b><u>Tavsiye</b></u>\n{"".join(f"* {guideline}{chr(10)}" for guideline in summary_json["fulfilling_destiny"]["guidelines"])}\n<b><u>Sorular</b></u>\n{"".join(f"* {question}{chr(10)}" for question in summary_json["fulfilling_destiny"]["questions"])}\n\n'

    summary_short += f'<b><u>Ünlü İnsanlar</b></u>\n{"".join(f"* {person}{chr(10)}" for person in summary_json["famous_people"])}'

    message = ""
    for part in summary_short.split("\n\n"):
        if len(message) + len(part) + 2 > 4096:
            await event.respond(message.strip(), parse_mode="html")
            message = ""
        message += f"\n\n{part}"
    else:
        await event.respond(message.strip(), parse_mode="html")


@client.on(events.CallbackQuery(pattern="summary\|(.*?)"))
async def paraphrased_summ(event) -> None:
    first, second = event.data.decode().split("|")[-1].split(",")
    life_path = (first, second)

    summary = life_path_to_content(
        life_path, Path("/home/nigella/tg_bot/Kitap/data/millman/tr/Summarizations/")
    )
    summary_paraphrased = paraphrase(summary)

    message = "<b><u>Genel Özet</b></u>"
    for part in summary_paraphrased.split("\n\n"):
        if len(message) + len(part) + 2 > 4096:
            await event.respond(message.strip(), parse_mode="html")
            message = ""
        message += f"\n\n{part}"
    else:
        await event.respond(message.strip(), parse_mode="html")


client.start()
print("Bot started...")
client.run_until_disconnected()
