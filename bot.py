from the_life import birthdate_to_life_path, life_path_to_content
from telethon import TelegramClient, events
from datetime import datetime
from pathlib import Path
import os
import re
import json

api_id = int(os.environ['OZETCIBOT_API_ID'])
api_hash = os.environ['OZETCIBOT_API_HASH']
bot_token = os.environ['OZETCIBOT_BOT_TOKEN']

print("-"*100)
print(f'{api_id=}, {api_hash=}, {bot_token=}')

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(pattern='/hayatyolu'))
async def handle_lifepath_command(event):
    message_raw = event.raw_text
    try:
        birthdate = datetime.strptime(message_raw.split('/hayatyolu')[1].strip(), '%d.%m.%Y')
    except Exception:
        await event.respond(f"Girilen mesaj ({message_raw}) hatalı!")
        return

    life_path = birthdate_to_life_path(birthdate)

    try:
        content = life_path_to_content(life_path, Path('/home/nigella/tg_bot/Kitap/data/tr/MDs/'))
    except Exception as e:
        await event.respond(f"Dosya işlemlerinde hata ile karşılaşıldı: {e}")
        return

    await event.respond(f"<b><u>HAYAT SAYISI</b></u>: {life_path[0]}/{life_path[1]}", parse_mode='html')

    for line in content.splitlines():
        if line.startswith('#'):
            content = content.replace(f'{line}\n', f"<b><u>{line.split('#')[-1].strip()}</b></u>")

    message = ''
    for part in content.split('\n\n'):
        if len(message) + len(part) + 2 > 4096:
            await event.respond(message.strip(), parse_mode="html")
            message = ''
        message += f'\n\n{part}'
    else:
        await event.respond(message.strip(), parse_mode="html")

    with open(f'/home/nigella/tg_bot/Kitap/data/tr/JSONs/{life_path[0]}_{life_path[1]}.json', 'r') as f:
        summary_json = json.loads(f.read())

    summary_short = '<b><u>Genel Kısa Özet</b></u>\n\n'

    summary_short += f'<b><u>Temel Özellikler</b></u>\n{"".join(f"- {key_trait}{chr(10)}" for key_trait in summary_json["key_traits"])}\n\n'

    summary_short += f'<b><u>Zorluklar</b></u>\n{"".join(f"- {challenge}{chr(10)}" for challenge in summary_json["challenges"])}\n\n'

    summary_short += f'<b><u>Fırsatlar</b></u>\n{"".join(f"- {opportunity}{chr(10)}" for opportunity in summary_json["opportunities"])}\n\n'

    summary_short += f'<b><u>Sağlık</b></u>\n<b><u>Pozitif</b></u>\n{"".join(f"- {positive}{chr(10)}" for positive in summary_json["health"]["positive"])}\n<b><u>Negatif</b></u>\n{"".join(f"- {negative}{chr(10)}" for negative in summary_json["health"]["negative"])}\n<b><u>Tavsiye</b></u>\n{"".join(f"- {advice}{chr(10)}" for advice in summary_json["health"]["advice"])}\n\n'

    summary_short += f'<b><u>İlişkiler</b></u>\n<b><u>Pozitif</b></u>\n{"".join(f"- {positive}{chr(10)}" for positive in summary_json["relationships"]["positive"])}\n<b><u>Negatif</b></u>\n{"".join(f"- {negative}{chr(10)}" for negative in summary_json["relationships"]["negative"])}\n<b><u>Tavsiye</b></u>\n{"".join(f"- {advice}{chr(10)}" for advice in summary_json["relationships"]["advice"])}\n\n'

    summary_short += f'<b><u>Yetenekler, İş ve Finans</b></u>\n<b><u>Pozitif</b></u>\n{"".join(f"- {positive}{chr(10)}" for positive in summary_json["talents_work_finances"]["positive"])}\n<b><u>Negatif</b></u>\n{"".join(f"- {negative}{chr(10)}" for negative in summary_json["talents_work_finances"]["negative"])}\n<b><u>Tavsiye</b></u>\n{"".join(f"- {advice}{chr(10)}" for advice in summary_json["talents_work_finances"]["advice"])}\n\n'

    summary_short += f'<b><u>Kaderini Gerçekleştirmek</b></u>\n<b><u>Tavsiye</b></u>\n{"".join(f"- {guideline}{chr(10)}" for guideline in summary_json["fulfilling_destiny"]["guidelines"])}\n<b><u>Sorular</b></u>\n{"".join(f"- {question}{chr(10)}" for question in summary_json["fulfilling_destiny"]["questions"])}\n\n'

    summary_short += f'<b><u>Ünlü İnsanlar</b></u>\n{"".join(f"- {person}{chr(10)}" for person in summary_json["famous_people"])}'

    message = ''
    for part in summary_short.split('\n\n'):
        if len(message) + len(part) + 2 > 4096:
            await event.respond(message.strip(), parse_mode="html")
            message = ''
        message += f'\n\n{part}'
    else:
        await event.respond(message.strip(), parse_mode="html")

    summary = life_path_to_content(life_path, Path('/home/nigella/tg_bot/Kitap/data/tr/Summarizations/'))

    message = '<b><u>Genel Özet</b></u>'
    for part in summary.split('\n\n'):
        if len(message) + len(part) + 2 > 4096:
            await event.respond(message.strip(), parse_mode="html")
            message = ''
        message += f'\n\n{part}'
    else:
        await event.respond(message.strip(), parse_mode="html")

client.start()
print("Bot started...")
client.run_until_disconnected()
