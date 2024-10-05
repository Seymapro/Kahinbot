# MIT License

# Copyright (c) 2024 Şeyma Yardım

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
import logging

__author__ = "Seymapro"
__version__ = "1.0.0"

logger = logging.getLogger("Kahin Bot")
logging.basicConfig(filename='/home/nigella/tg_bot/Kitap/ozetcibot.log', level=logging.INFO, format="%(name)s - %(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s")

api_id = int(os.environ["OZETCIBOT_API_ID"])
api_hash = os.environ["OZETCIBOT_API_HASH"]
bot_token = os.environ["OZETCIBOT_BOT_TOKEN"]

client = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)

USER_DATA = {}

def create_json_summary(content_json: dict, key: str) -> str:
    TRANSLATIONS = {
        "challenges": "<b><u>ZORLUKLAR</b></u>",
        "famous_people": "<b><u>ÜNLÜ İNSANLAR</b></u>",
        "fulfilling_destiny": "<b><u>KADERİNİ GERÇEKLEŞTİRMEK</b></u>",
        "guidelines": "<b><u>TAVSİYELER</b></u>",
        "questions": "<b><u>SORULAR</b></u>",
        "health": "<b><u>SAĞLIK</b></u>",
        "advice": "<b><u>TAVSİYELER</b></u>",
        "positive": "<b><u>POZİTİF YÖNLER</b></u>",
        "negative": "<b><u>NEGATİF YÖNLER</b></u>",
        "key_traits": "<b><u>TEMEL ÖZELLİKLER</b></u>",
        "opportunities": "<b><u>FIRSATLAR</b></u>",
        "relationships": "<b><u>İLİŞKİLER</b></u>",
        "talents_work_finances": "<b><u>YETENEKLER, İŞ VE FİNANS</b></u>",
    }

    content = ""

    if type(content_json[key]) is list:
        if content_json[key]:
            content += TRANSLATIONS[key] + "\n\n"
            content += "\n".join([f"- {bulletpoint}" for bulletpoint in content_json[key]]) + "\n\n"
    else:
        content += TRANSLATIONS[key] + "\n\n"

        for subtitle, bulletpoints in content_json[key].items():
            if bulletpoints:
                content += TRANSLATIONS[subtitle] + "\n\n"
                content += "\n".join([f"- {bulletpoint}" for bulletpoint in bulletpoints]) + "\n\n"

    return content

async def send_message(event, content: str) -> None:
    message = ""
    for part in content.split("\n\n"):
        if len(message) + len(part) + 2 > 4096:
            await client.send_message(message=message.strip(), parse_mode="html", entity=await event.get_chat(), reply_to=USER_DATA[event.sender_id]["message_id"])
            message = ""
        message += f"\n\n{part}"
    else:
        if not message.isspace():
            await client.send_message(message=message.strip(), parse_mode="html", entity=await event.get_chat(), reply_to=USER_DATA[event.sender_id]["message_id"])

    life_path = USER_DATA[event.sender_id]["life_path"]
    await client.send_message(
        message=f"<b><u>HAYAT SAYISI</b></u>: {life_path[0]}/{life_path[1]}",
        reply_to=USER_DATA[event.sender_id]["message_id"],
        entity=await event.get_chat(),
        buttons=[
            [Button.inline("Tam Metin (Millman)", f"full_text_millman")],
            [Button.inline("Tam Metin (Forbes)", f"full_text_forbes")],
            [Button.inline("Özet (Millman)", f"summary_millman")],
            [Button.inline("Özet (Forbes)", f"summary_forbes")],
            [Button.inline("Maddeler (Millman)", f"json_millman")],
        ],
        parse_mode="html",
    )

@client.on(events.NewMessage(incoming=True, pattern=r"([\s\S]*)\d{2}\.\d{2}\.\d{4}([\s\S]*)"))
async def handle_birthdate(event) -> None:
    logger.info(event)

    message_raw = event.raw_text.strip()
    try:
        birthdate = datetime.strptime(message_raw, "%d.%m.%Y")
    except Exception:
        await event.reply(f"Girilen mesaj ({message_raw}) hatalı!")
        return

    life_path = birthdate_to_life_path(birthdate)

    USER_DATA[event.message.sender_id] = {"message_id": event.message.id,
                                          "life_path": life_path}

    await send_message(event, "")

@client.on(events.CallbackQuery(pattern=r"full_text_millman"))
async def send_full_text_millman(event) -> None:
    life_path = USER_DATA[event.sender_id]["life_path"]

    try:
        content = life_path_to_content(
            life_path, Path("/home/nigella/tg_bot/Kitap/data/millman/tr/MDs/")
        )
    except FileNotFoundError as e:
        await client.send_message(message=f"Dosya işlemlerinde hata ile karşılaşıldı: {e}", entity=await event.get_chat(), reply_to=USER_DATA[event.sender_id]["message_id"])
        return

    for line in content.splitlines():
        if line.startswith("#"):
            content = content.replace(
                f"{line}\n", f"<b><u>{line.split('#')[-1].strip()}</b></u>"
            )

    await send_message(event, content)

@client.on(events.CallbackQuery(pattern=r"full_text_forbes"))
async def send_full_text_forbes(event) -> None:
    await send_message(event, "Henüz yapım aşamasında.")

@client.on(events.CallbackQuery(pattern=r"json_millman"))
async def send_json_summary(event) -> None:
    life_path = USER_DATA[event.sender_id]["life_path"]

    try:
        with open(
            f"/home/nigella/tg_bot/Kitap/data/millman/tr/JSONs/{life_path[0]}_{life_path[1]}.json",
            "r",
        ) as f:
            summary_json = json.loads(f.read())
    except FileNotFoundError as e:
        await client.send_message(message=f"Dosya işlemlerinde hata ile karşılaşıldı: {e}", entity=await event.get_chat(), reply_to=USER_DATA[event.sender_id]["message_id"])
        return

    summary_short = "<b><u>GENEL KISA ÖZET</b></u>\n\n"

    summary_short += create_json_summary(summary_json, "key_traits")
    summary_short += create_json_summary(summary_json, "challenges")
    summary_short += create_json_summary(summary_json, "opportunities")
    summary_short += create_json_summary(summary_json, "health")
    summary_short += create_json_summary(summary_json, "relationships")
    summary_short += create_json_summary(summary_json, "talents_work_finances")
    summary_short += create_json_summary(summary_json, "fulfilling_destiny")
    summary_short += create_json_summary(summary_json, "famous_people")

    await send_message(event, summary_short.strip())

@client.on(events.CallbackQuery(pattern=r"summary_millman"))
async def send_paraphrased_summary_millman(event) -> None:
    life_path = USER_DATA[event.sender_id]["life_path"]

    try:
        summary = life_path_to_content(
            life_path, Path("/home/nigella/tg_bot/Kitap/data/millman/tr/Summarizations/")
        )
    except FileNotFoundError as e:
        await client.send_message(message=f"Dosya işlemlerinde hata ile karşılaşıldı: {e}", entity=await event.get_chat(), reply_to=USER_DATA[event.sender_id]["message_id"])
        return

    await send_message(event, f"<b><u>GENEL ÖZET</b></u>\n{paraphrase(summary)}")

@client.on(events.CallbackQuery(pattern=r"summary_forbes"))
async def send_paraphrased_summary_forbes(event) -> None:
    await send_message(event, "Henüz yapım aşamasında.")

client.run_until_disconnected()
