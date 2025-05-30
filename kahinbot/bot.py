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

"""A Telegram bot for providing personalized numerological and astrological readings.

This module implements a Telegram bot that offers various types of readings based on
a user's birthdate, including:
- Life path number calculations and interpretations (Millman method)
- PIN code generation and analysis (Forbes method)
- Zodiac sign traits and Enneagram type correlations
- Multiple reading formats:
    - Full detailed readings
    - Summarized versions
    - Bullet-point overviews
    - Paraphrased summaries

The bot handles user interactions via Telegram's callback query system and formats
all responses using HTML for improved readability. Content is stored in separate
data files (JSON, Markdown) and accessed based on user input.

Typical usage:
    python bot.py

Requirements:
    - Telegram API credentials in environment variables:
        KAHIN_BOT_API_ID
        KAHIN_BOT_API_HASH
        KAHIN_BOT_BOT_TOKEN
    - Data files in ../data/ directory structure
    - Python packages: telethon, logging

Attributes:
    logger (Logger): Module-level logger instance
    API_ID (int): Telegram API ID from environment
    API_HASH (str): Telegram API hash from environment
    BOT_TOKEN (str): Telegram bot token from environment
    client (TelegramClient): Bot's Telegram client instance
    user_data (dict): Runtime storage of user session data
"""

from the_life import birthdate_to_life_path, life_path_to_content
from pin_code import get_pin_code, pin_code_to_contents
from paraphraser import paraphrase
from zodiac import Zodiac
from telethon import TelegramClient, events, Button
from datetime import datetime
from pathlib import Path
import os
import json
import logging

__author__ = "Seymapro"
__version__ = "1.1.0"

logger = logging.getLogger("Kahin Bot")
logging.basicConfig(
    filename="../kahin-bot.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s @ (%(name)s:%(module)s:%(funcName)s:%(lineno)d) # %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Load environment variables for Telegram API credentials
API_ID = int(os.environ["KAHIN_BOT_API_ID"])
API_HASH = os.environ["KAHIN_BOT_API_HASH"]
BOT_TOKEN = os.environ["KAHIN_BOT_BOT_TOKEN"]

# Initialize the Telegram client with the bot token
client = TelegramClient("bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Dictionary to store user data, including their life path and message IDs
user_data: dict[int, dict[str, int | tuple[int, int]]] = {}


# TODO: Fix repetition.
def create_json_summary(content_json: dict[str, list[str]] | dict[str, dict[str, list[str]]], key: str) -> str:
    """Creates a formatted summary string from a JSON object containing numerological readings.

    Formats the content from a JSON structure into a human-readable HTML-formatted string.
    Handles both simple list structures and nested dictionary structures, converting them
    into bullet-point lists with translated Turkish headers.

    Args:
        content_json: A dictionary containing either:
            - A mapping of section names to lists of bullet points, or
            - A mapping of section names to dictionaries of subsection names and their bullet points
        key: The section name to process from the content_json

    Returns:
        A formatted string containing the summary information with HTML formatting.
        The string includes translated headers in bold and underlined format,
        followed by bullet-pointed lists of content.

    Examples:
        Simple list structure:
            >>> json = {"key_traits": ["Confident", "Creative"]}
            >>> create_json_summary(json, "key_traits")
            '<b><u>TEMEL ÖZELLİKLER</b></u>\n\n- Confident\n- Creative\n\n'

        Nested dictionary structure:
            >>> json = {"health": {"positive": ["Energetic"], "negative": ["Stressed"]}}
            >>> create_json_summary(json, "health")
            '<b><u>SAĞLIK</b></u>\n\n<b><u>POZİTİF YÖNLER</b></u>\n\n- Energetic\n\n<b><u>NEGATİF YÖNLER</b></u>\n\n- Stressed\n\n'
    """
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


# TODO: Fix repetition.
async def send_message(
    event: events.callbackquery.CallbackQuery | events.newmessage.NewMessage,
    content: str,
    show_buttons: bool = True,
) -> None:
    """Sends message to a Telegram chat with content splitting and optional navigation buttons.

    Handles sending long messages by automatically splitting them into chunks of 4096 characters
    (Telegram's message length limit). Can optionally display navigation buttons showing user info
    and reading options.

    Args:
        event: Telegram event from either a callback query or new message. Used to determine
            the chat and message to reply to.
        content: The message text to send. Will be split into chunks if longer than 4096 chars.
            Supports HTML formatting.
        show_buttons: If True, appends navigation buttons and user info after the message.
            Default is True.

    Each message is sent as a reply to the original user message and includes HTML parsing.
    When show_buttons is True, displays user's:
        - Life path number
        - PIN code
        - Zodiac sign
        - Enneagram value
    Along with navigation buttons for different reading options.

    Messages are split on double newlines (\n\n) to preserve formatting when chunking.
    Empty or whitespace-only messages are skipped.
    """

    message = ""
    for part in content.split("\n\n"):
        if len(message) + len(part) + 2 > 4096:
            await client.send_message(
                entity=await event.get_chat(),
                message=message.strip(),
                reply_to=user_data[event.sender_id]["message_id"],
                parse_mode="html",
            )
            message = ""
        message += f"\n\n{part}"
    else:
        if not message.isspace():
            await client.send_message(
                entity=await event.get_chat(),
                message=message.strip(),
                reply_to=user_data[event.sender_id]["message_id"],
                parse_mode="html",
            )

    if show_buttons:
        life_path: tuple[int, int] = user_data[event.sender_id]["life_path"]
        pin_code: list[int] = user_data[event.sender_id]["pin_code"]
        zodiac_sign: str = user_data[event.sender_id]["zodiac_sign"]

        await client.send_message(
            entity=await event.get_chat(),
            message=f"<b><u>HAYAT SAYISI</b></u>: {life_path[0]}/{life_path[1]}\n"
            + f"<b><u>PİN KODU</b></u>: {''.join(map(str, pin_code))}\n"
            + f"<b><u>BURÇ</b></u>: {zodiac_sign.sign}\n"
            + f"<b><u>BURCUN ENNEAGRAM DEĞERİ</b></u>: {zodiac_sign.enneagram}",
            reply_to=user_data[event.sender_id]["message_id"],
            parse_mode="html",
            buttons=[
                [Button.inline("Tam Metin (Millman)", "full_text_millman")],
                [Button.inline("Tam Metin (Forbes)", "full_text_forbes")],
                [Button.inline("Özet (Millman)", "summary_millman")],
                [Button.inline("Özet (Forbes)", "summary_forbes")],
                [Button.inline("Kısa Maddeler (Millman)", "json_short_millman")],
                [Button.inline("Uzun Maddeler (Millman)", "json_long_millman")],
                [Button.inline("Enneagram Özellikleri", "zodiac_traits")],
            ],
        )


@client.on(events.NewMessage(incoming=True, pattern=r"([\s\S]*)\d{2}\.\d{2}\.\d{4}([\s\S]*)"))
async def handle_birthdate(event: events.newmessage.NewMessage) -> None:
    """Process incoming messages containing birthdates and initialize user data for numerological readings.

    This handler is triggered by messages containing dates in DD.MM.YYYY format. It parses the birthdate,
    calculates numerological values (life path, PIN code), determines zodiac sign, and stores this
    information in the user_data dictionary for subsequent readings.

    Args:
        event: The Telegram message event containing a birthdate string. Expected to have attributes:
            - raw_text: The message text containing the birthdate
            - message.sender_id: Unique identifier for the message sender
            - message.id: Unique identifier for the message

    Side Effects:
        - Logs the event at INFO level
        - Updates the global user_data dictionary with user's numerological information
        - Sends error messages to user via Telegram on parsing failures
        - Logs errors at ERROR level when exceptions occur

    Error Handling:
        - ValueError: When birthdate format is invalid (responds with error message)
        - Other exceptions: Logs error and notifies user of system error

    Example:
        When a user sends "25.12.1990", the function will:
        1. Parse the date
        2. Calculate life path number
        3. Generate PIN code
        4. Determine zodiac sign
        5. Store all data for future readings
    """

    logger.info(event)

    message_raw: str = event.raw_text.strip()
    try:
        birthdate = datetime.strptime(message_raw, "%d.%m.%Y")
    except ValueError:
        await event.reply(f"Girilen mesaj ({message_raw}) hatalı!")

        return None
    except Exception as err:
        await event.reply("Bilinmeyen bir hata ile karşılaşıldı ve yöneticiye haber verildi.")
        logger.error(err)

        return None

    life_path = birthdate_to_life_path(birthdate)
    pin_code = get_pin_code(birthdate)
    zodiac_sign = Zodiac(birthdate)

    user_data[event.message.sender_id] = {
        "message_id": event.message.id,
        "life_path": life_path,
        "pin_code": pin_code,
        "birthdate": birthdate,
        "zodiac_sign": zodiac_sign,
    }

    await send_message(event, "")


@client.on(events.CallbackQuery(pattern=r"full_text_millman"))
async def send_full_text_millman(event: events.callbackquery.CallbackQuery) -> None:
    """Sends the complete numerological reading text from Millman's source to the user.

    Retrieves the full text based on the user's life path number, formats the content
    by converting markdown-style headers into HTML-formatted bold and underlined text,
    and sends the result as a Telegram message.

    Args:
        event: Telegram callback query event containing:
            - sender_id: User identifier to retrieve stored life path number
            - Other event data needed for message handling

    Raises:
        FileNotFoundError: When the content file for the life path number is not found
        Exception: For any other unexpected errors during processing

    Side Effects:
        - Logs errors to the configured logger
        - Sends error messages to user when file operations fail
        - Sends formatted content to user via Telegram

    Notes:
        - Content is read from ../data/millman/tr/MDs/
        - Headers starting with '#' are converted to HTML <b><u> tags
        - Messages are split and sent in chunks if they exceed Telegram's length limit
    """

    life_path: tuple[int, int] = user_data[event.sender_id]["life_path"]

    # TODO: Extract the file operations with error handling logic to a different function so it is cleaner.
    try:
        content = life_path_to_content(life_path, Path("../data/millman/tr/MDs/"))
    except FileNotFoundError as err:
        await send_message(
            event,
            "Dosya işlemlerinde hata ile karşılaşıldı, sorun yöneticiye bildirildi.",
        )
        logger.error(err)

        return None
    except Exception as err:
        await send_message(event, "Bilinmeyen bir hata ile karşılaşıldı ve yöneticiye haber verildi.")
        logger.error(err)

        return None

    # TODO: Change the actual data so we won't have to edit it on-fly like this.
    for line in content.splitlines():
        if line.startswith("#"):
            content = content.replace(f"{line}\n", f"<b><u>{line.split('#')[-1].strip()}</b></u>")

    await send_message(event, content)


@client.on(events.CallbackQuery(pattern=r"full_text_forbes"))
async def send_full_text_forbes(event: events.callbackquery.CallbackQuery) -> None:
    """Sends the complete numerological reading text from Forbes' source based on the user's PIN code.

    Retrieves the full text content for each digit in the user's PIN code from Forbes' source files,
    combines them into a single message, formats any markdown-style headers into HTML formatting,
    and sends the result via Telegram.

    Args:
        event: Telegram callback query event containing:
            - sender_id: User identifier to retrieve stored PIN code
            - Other event data needed for message handling

    File Operations:
        - Reads content from ../data/forbes/tr/MDs/ directory
        - Each PIN code digit corresponds to a separate content file
        - Files are combined in PIN code digit order

    Text Processing:
        - Combines multiple content files with double newline separation
        - Converts markdown headers (#) to HTML <b><u> formatted text
        - Maintains original formatting and structure of content

    Error Handling:
        - FileNotFoundError: When content files for PIN digits are not found
        - General exceptions: For other processing errors
        - Sends user-friendly error messages while logging details

    Side Effects:
        - Logs errors to the configured logger
        - Sends messages via Telegram
        - Updates user interaction state
    """
    pin_code: list[int] = user_data[event.sender_id]["pin_code"]

    # TODO: Extract the file operations with error handling logic to a different function so it is cleaner.
    try:
        contents = pin_code_to_contents(pin_code, Path("../data/forbes/tr/MDs/"))
    except FileNotFoundError as err:
        await send_message(
            event,
            "Dosya işlemlerinde hata ile karşılaşıldı, sorun yöneticiye bildirildi.",
        )
        logger.error(err)

        return None
    except Exception as err:
        await send_message(event, "Bilinmeyen bir hata ile karşılaşıldı ve yöneticiye haber verildi.")
        logger.error(err)

        return None

    content = "\n\n".join(contents).strip()

    # TODO: Change the actual data so we won't have to edit it on-fly like this.
    for line in content.splitlines():
        if line.startswith("#"):
            content = content.replace(f"{line}", f"<b><u>{line.split('#')[-1].strip()}</b></u>")

    await send_message(event, content)


@client.on(events.CallbackQuery(pattern=r"json_short_millman"))
async def send_json_short_summary_millman(
    event: events.callbackquery.CallbackQuery,
) -> None:
    """Sends a concise bullet-point summary of Millman numerology reading based on life path number.

    Retrieves and formats pre-structured JSON data containing key aspects of the numerological reading
    organized into categories like traits, challenges, health, etc. The content is formatted with
    HTML tags for Telegram display.

    Args:
        event: Telegram callback query event containing:
            - sender_id: Used to retrieve user's stored life path number
            - Other event data needed for message handling

    Raises:
        FileNotFoundError: When JSON file for life path number doesn't exist
        Exception: For other errors during file operations or message sending

    Side Effects:
        - Reads JSON file from ../data/millman/tr/JSONs/ directory
        - Sends multiple Telegram messages to user
        - Logs errors to configured logger
        - Updates user interaction state

    Example JSON structure:
        {
            "key_traits": ["trait1", "trait2"],
            "health": {
                "positive": ["good1", "good2"],
                "negative": ["bad1", "bad2"]
            }
            // ... other categories
        }
    """
    life_path: tuple[int, int] = user_data[event.sender_id]["life_path"]

    # TODO: Extract the file operations with error handling logic to a different function so it is cleaner.
    try:
        with open(
            f"../data/millman/tr/JSONs/{life_path[0]}_{life_path[1]}.json",
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
    except Exception as err:
        await send_message(event, "Bilinmeyen bir hata ile karşılaşıldı ve yöneticiye haber verildi.")
        logger.error(err)

        return None

    # I know it looks disgusting but it works and we can't get rid of it reliably, at least not if
    # we want the final data to be in a proper format with good ordering of headings.
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


@client.on(events.CallbackQuery(pattern=r"json_long_millman"))
async def send_json_long_summary_millman(
    event: events.callbackquery.CallbackQuery,
) -> None:
    """Sends a detailed bullet-point summary of Millman numerology reading using extended JSON data.

    Retrieves extended JSON data for the user's life path number and formats it into a structured
    message with categorized bullet points. Covers detailed aspects of personality traits,
    challenges, opportunities, health, relationships, talents, destiny, and notable people
    with the same life path number.

    Args:
        event: Telegram callback query event containing:
            - sender_id: Used to retrieve user's life path number from user_data
            - Other event metadata needed for sending messages

    Side Effects:
        - Reads JSON file from ../data/millman/tr/JSONs_Extended/ directory
        - Sends formatted messages via Telegram
        - Logs errors if file operations fail

    Error Handling:
        - FileNotFoundError: When JSON file for life path doesn't exist
        - Other exceptions: For unexpected errors during processing
        Both cases result in user-friendly error messages and error logging

    Message Format:
        The output is formatted with HTML tags and includes:
        - Main title "GENEL UZUN ÖZET"
        - Multiple sections with translated Turkish headers
        - Bullet-pointed lists under each section
        - Navigation buttons after content (via send_message)
    """
    life_path: tuple[int, int] = user_data[event.sender_id]["life_path"]

    # TODO: Extract the file operations with error handling logic to a different function so it is cleaner.
    try:
        with open(
            f"../data/millman/tr/JSONs_Extended/{life_path[0]}_{life_path[1]}.json",
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
    except Exception as err:
        await send_message(event, "Bilinmeyen bir hata ile karşılaşıldı ve yöneticiye haber verildi.")
        logger.error(err)

        return None

    # I know it looks disgusting but it works and we can't get rid of it reliably, at least not if
    # we want the final data to be in a proper format with good ordering of headings.
    summary_short = "<b><u>GENEL UZUN ÖZET</b></u>\n\n"
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
async def send_paraphrased_summary_millman(
    event: events.callbackquery.CallbackQuery,
) -> None:
    """Sends a paraphrased summary of Millman numerology reading based on user's life path number.

    Retrieves the summarized content from the Millman source, processes it through a paraphrasing
    engine, and sends the result as a Telegram message. Shows a loading message while processing.

    Args:
        event: Telegram callback query event containing:
            - sender_id: User identifier to retrieve stored life path number
            - Other event data needed for message handling

    Raises:
        FileNotFoundError: When summary file for life path number doesn't exist
        Exception: For other errors during file operations or message sending

    Side Effects:
        - Reads summary file from ../data/millman/tr/Summarizations/ directory
        - Sends two Telegram messages:
            1. A loading message
            2. The paraphrased summary with HTML formatting
        - Logs errors to configured logger if any occur

    The final message is formatted with an HTML header and the paraphrased content.
    If errors occur, sends user-friendly error messages while logging the details.
    """

    life_path: tuple[int, int] = user_data[event.sender_id]["life_path"]

    try:
        summary = life_path_to_content(
            life_path,
            Path("../data/millman/tr/Summarizations/"),
        )
    except FileNotFoundError as err:
        await send_message(
            event,
            "Dosya işlemlerinde hata ile karşılaşıldı, sorun yöneticiye bildirildi.",
        )
        logger.error(err)

        return None
    except Exception as err:
        await send_message(event, "Bilinmeyen bir hata ile karşılaşıldı ve yöneticiye haber verildi.")
        logger.error(err)

        return None

    await send_message(event, "Genel özet hazırlanıyor, lütfen bekleyiniz...", show_buttons=False)
    await send_message(event, f"<b><u>GENEL ÖZET</b></u>\n{paraphrase(summary)}")


@client.on(events.CallbackQuery(pattern=r"summary_forbes"))
async def send_paraphrased_summary_forbes(
    event: events.callbackquery.CallbackQuery,
) -> None:
    """Sends a paraphrased summary of Forbes numerology reading based on user's PIN code.

    Retrieves summarized content files for each digit in the user's PIN code from Forbes'
    source, combines them, processes through a paraphrasing engine, and sends the result
    as a formatted Telegram message.

    Args:
        event: Telegram callback query event containing:
            - sender_id: Used to retrieve user's stored PIN code
            - Other event metadata needed for message handling

    Raises:
        FileNotFoundError: When summary files for PIN code digits don't exist
        Exception: For any other unexpected errors during processing

    Side Effects:
        - Reads summary files from ../data/forbes/tr/Summarizations/ directory
        - Sends multiple Telegram messages:
            1. A loading status message
            2. The final paraphrased content with HTML formatting
        - Logs errors to configured logger
        - Updates user message history

    The final message combines summaries for all PIN digits, adds HTML formatting,
    and applies paraphrasing for improved readability. User-friendly error messages
    are sent while detailed errors are logged if any issues occur.
    """

    pin_code: list[int] = user_data[event.sender_id]["pin_code"]

    try:
        contents = pin_code_to_contents(
            pin_code,
            Path("../data/forbes/tr/Summarizations/"),
        )
    except FileNotFoundError as err:
        await send_message(
            event,
            "Dosya işlemlerinde hata ile karşılaşıldı, sorun yöneticiye bildirildi.",
        )
        logger.error(err)

        return None
    except Exception as err:
        await send_message(event, "Bilinmeyen bir hata ile karşılaşıldı ve yöneticiye haber verildi.")
        logger.error(err)

        return None

    await send_message(event, "Genel özet hazırlanıyor, lütfen bekleyiniz...", show_buttons=False)

    content = "\n\n".join(contents).strip()
    await send_message(event, f"<b><u>GENEL ÖZET</b></u>\n{paraphrase(content)}")


@client.on(events.CallbackQuery(pattern=r"zodiac_traits"))
async def send_zodiac(
    event: events.callbackquery.CallbackQuery,
) -> None:
    """Sends formatted zodiac sign traits and Enneagram information for the user.

    Retrieves the user's zodiac sign information from stored user data and formats it
    for display in Telegram. Converts section headers (lines starting with #) to HTML-
    formatted bold and underlined text.

    Args:
        event: Telegram callback query event containing:
            - sender_id: User identifier to retrieve stored zodiac info
            - Other event data needed for message handling

    Side Effects:
        - Retrieves zodiac data from user_data global dictionary
        - Sends formatted message via Telegram using send_message helper
        - Formats markdown-style headers to HTML

    The message includes:
        - Basic zodiac sign information
        - Associated Enneagram type details
        - Characteristic traits
        All formatted with HTML tags for Telegram display
    """
    zodiac_sign: list[tuple] = user_data[event.sender_id]["zodiac_sign"]

    content = str(zodiac_sign)

    # TODO: This is not a todo actually, i love my data as the way it is <3
    for line in content.splitlines():
        if line.startswith("#"):
            content = content.replace(f"{line}", f"<b><u>{line.split('#')[-1].strip()}</b></u>")

    await send_message(event, content)


client.run_until_disconnected()
