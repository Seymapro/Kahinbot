from the_life import birthdate_to_life_path, life_path_to_content
from telethon import TelegramClient, events
from datetime import datetime
from pathlib import Path
import os

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
        print(birthdate)
    except Exception:
        await event.respond(f"Girilen mesaj ({message_raw}) hatalı!")
        return

    life_path = birthdate_to_life_path(birthdate)
    print(life_path)

    try:
        content = life_path_to_content(life_path,Path('/home/nigella/tg_bot/Kitap/data/MDs/'))
        print(content)
    except Exception as e:
        await event.respond(f"Dosya işlemlerinde hata ile karşılaşıldı: {e}")
        return

    await event.respond(f"**Hayat Sayısı**: {life_path}", parse_mode='markdown')

    for i in range(0, len(content), 4096):
        await event.respond(f"{content[i:min(i+4096, len(content))]}", parse_mode='markdown')

client.start()
print("Bot started...")
client.run_until_disconnected()
