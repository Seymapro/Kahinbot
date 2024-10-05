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
from telethon import TelegramClient, events, Button  # type: ignore[reportAttributeAccessIssue, reportUnknownVariableType]
from datetime import datetime
from pathlib import Path
import os
import json
import logging

__author__ = "Seymapro"
__version__ = "1.0.0"

logger = logging.getLogger("Kahin Bot")
logging.basicConfig(
    filename="/home/nigella/tg_bot/Kitap/kahin_bot.log",
    level=logging.INFO,
    format="%(name)s - %(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s",
)

api_id = int(os.environ["KAHIN_BOT_API_ID"])
api_hash = os.environ["KAHIN_BOT_API_HASH"]
bot_token = os.environ["KAHIN_BOT_BOT_TOKEN"]

client = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)

USER_DATA: dict[int, dict[str, int | tuple[int, int]]] = {}


def create_json_summary(
    content_json: dict[str, list[str]] | dict[str, dict[str, list[str]]], key: str
) -> str:
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
            content += (
                "\n".join([f"- {bulletpoint}" for bulletpoint in content_json[key]])
                + "\n\n"
            )
    else:
        content += TRANSLATIONS[key] + "\n\n"

        for subtitle, bulletpoints in content_json[key].items():  # type: ignore[reportUnknownMemberType, reportAttributeAccessIssue]
            if bulletpoints:
                content += TRANSLATIONS[subtitle] + "\n\n"
                content += (
                    "\n".join([f"- {bulletpoint}" for bulletpoint in bulletpoints])  # type: ignore[reportUnknownVariableType]
                    + "\n\n"
                )

    return content


async def send_message(
    event: events.callbackquery.CallbackQuery | events.newmessage.NewMessage,
    content: str,
) -> None:
    if not content:
        return None

    message = ""
    for part in content.split("\n\n"):
        if len(message) + len(part) + 2 > 4096:
            await client.send_message(  # type: ignore[reportUnknownMemberType]
                entity=await event.get_chat(),  # type: ignore[reportUnknownArgumentType, reportUnknownMemberType]
                message=message.strip(),
                reply_to=USER_DATA[event.sender_id]["message_id"],  # type: ignore[reportArgumentType, reportUnknownMemberType]
                parse_mode="html",
            )
            message = ""
        message += f"\n\n{part}"
    else:
        await client.send_message(  # type: ignore[reportUnknownMemberType]
            entity=await event.get_chat(),  # type: ignore[reportUnknownArgumentType, reportUnknownMemberType]
            message=message.strip(),
            reply_to=USER_DATA[event.sender_id]["message_id"],  # type: ignore[reportArgumentType, reportUnknownMemberType]
            parse_mode="html",
        )

    life_path: tuple[int, int] = USER_DATA[event.sender_id]["life_path"]  # type: ignore[reportUnknownMemberType]
    await client.send_message(  # type: ignore[reportUnknownMemberType]
        entity=await event.get_chat(),  # type: ignore[reportUnknownArgumentType, reportUnknownMemberType]
        message=f"<b><u>HAYAT SAYISI</b></u>: {life_path[0]}/{life_path[1]}",
        reply_to=USER_DATA[event.sender_id]["message_id"],  # type: ignore[reportArgumentType, reportUnknownMemberType]
        parse_mode="html",
        buttons=[
            [Button.inline("Tam Metin (Millman)", "full_text_millman")],  # type: ignore[reportUnknownMemberType]
            [Button.inline("Tam Metin (Forbes)", "full_text_forbes")],  # type: ignore[reportUnknownMemberType]
            [Button.inline("Özet (Millman)", "summary_millman")],  # type: ignore[reportUnknownMemberType]
            [Button.inline("Özet (Forbes)", "summary_forbes")],  # type: ignore[reportUnknownMemberType]
            [Button.inline("Maddeler (Millman)", "json_millman")],  # type: ignore[reportUnknownMemberType]
        ],
    )


@client.on(  # type: ignore[reportUnknownMemberType, reportUntypedFunctionDecorator]
    events.NewMessage(incoming=True, pattern=r"([\s\S]*)\d{2}\.\d{2}\.\d{4}([\s\S]*)")  # type: ignore[reportAttributeAccessIssue, reportUnknownArgumentType, reportUnknownMemberType]
)
async def handle_birthdate(event: events.newmessage.NewMessage) -> None:
    logger.info(event)

    message_raw: str = event.raw_text.strip()  # type: ignore[reportAttributeAccessIssue, reportUnknownMemberType, reportUnknownVariableType]
    try:
        birthdate = datetime.strptime(message_raw, "%d.%m.%Y")  # type: ignore[reportUnknownArgumentType]
    except Exception:
        await event.reply(f"Girilen mesaj ({message_raw}) hatalı!")  # type: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
        return None

    life_path = birthdate_to_life_path(birthdate)

    USER_DATA[event.message.sender_id] = {  # type: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
        "message_id": event.message.id,  # type: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
        "life_path": life_path,
    }

    await send_message(event, "")


@client.on(events.CallbackQuery(pattern=r"full_text_millman"))  # type: ignore[reportAttributeAccessIssue, reportUnknownArgumentType, reportUnknownMemberType, reportUntypedFunctionDecorator]
async def send_full_text_millman(event: events.callbackquery.CallbackQuery) -> None:
    life_path: tuple[int, int] = USER_DATA[event.sender_id]["life_path"]  # type: ignore[reportAttributeAccessIssue, reportUnknownMemberType]

    try:
        content = life_path_to_content(
            life_path, Path("/home/nigella/tg_bot/Kitap/data/millman/tr/MDs/")
        )
    except FileNotFoundError as err:
        await send_message(
            event,
            "Dosya işlemlerinde hata ile karşılaşıldı, sorun yöneticiye bildirildi.",
        )
        logger.error(err)
        return None

    for line in content.splitlines():
        if line.startswith("#"):
            content = content.replace(
                f"{line}\n", f"<b><u>{line.split('#')[-1].strip()}</b></u>"
            )

    await send_message(event, content)


@client.on(events.CallbackQuery(pattern=r"full_text_forbes"))  # type: ignore[reportAttributeAccessIssue, reportUnknownArgumentType, reportUnknownMemberType, reportUntypedFunctionDecorator]
async def send_full_text_forbes(event: events.callbackquery.CallbackQuery) -> None:
    await send_message(event, "Henüz yapım aşamasında.")


@client.on(events.CallbackQuery(pattern=r"json_millman"))  # type: ignore[reportAttributeAccessIssue, reportUnknownArgumentType, reportUnknownMemberType, reportUntypedFunctionDecorator]
async def send_json_summary_millman(event: events.callbackquery.CallbackQuery) -> None:
    life_path: tuple[int, int] = USER_DATA[event.sender_id]["life_path"]  # type: ignore[reportAttributeAccessIssue, reportUnknownMemberType]

    try:
        with open(
            f"/home/nigella/tg_bot/Kitap/data/millman/tr/JSONs/{life_path[0]}_{life_path[1]}.json",
            "r",
        ) as f:
            summary_json = json.loads(f.read())
    except FileNotFoundError as err:
        await send_message(
            event,
            "Dosya işlemlerinde hata ile karşılaşıldı, sorun yöneticiye bildirildi.",
        )
        logger.error(err)
        return None

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


@client.on(events.CallbackQuery(pattern=r"summary_millman"))  # type: ignore[reportAttributeAccessIssue, reportUnknownArgumentType, reportUnknownMemberType, reportUntypedFunctionDecorator]
async def send_paraphrased_summary_millman(
    event: events.callbackquery.CallbackQuery,
) -> None:
    life_path: tuple[int, int] = USER_DATA[event.sender_id]["life_path"]  # type: ignore[reportAttributeAccessIssue, reportUnknownMemberType]

    try:
        summary = life_path_to_content(
            life_path,
            Path("/home/nigella/tg_bot/Kitap/data/millman/tr/Summarizations/"),
        )
    except FileNotFoundError as err:
        await send_message(
            event,
            "Dosya işlemlerinde hata ile karşılaşıldı, sorun yöneticiye bildirildi.",
        )
        logger.error(err)
        return None

    await send_message(event, f"<b><u>GENEL ÖZET</b></u>\n{paraphrase(summary)}")


@client.on(events.CallbackQuery(pattern=r"summary_forbes"))  # type: ignore[reportAttributeAccessIssue, reportUnknownArgumentType, reportUnknownMemberType, reportUntypedFunctionDecorator]
async def send_paraphrased_summary_forbes(
    event: events.callbackquery.CallbackQuery,
) -> None:
    await send_message(event, "Henüz yapım aşamasında.")


client.run_until_disconnected()  # type: ignore[reportUnknownMemberType]
