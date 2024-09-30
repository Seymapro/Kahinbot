from the_life import birthdate_to_life_path, life_path_to_content
from telethon import TelegramClient, events
from datetime import datetime
from pathlib import Path
import os

api_id = int(os.environ['OZETCIBOT_API_ID'])
api_hash = os.environ['OZETCIBOT_API_HASH']
bot_token = os.environ['OZETCIBOT_BOT_TOKEN']

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(pattern='/hayatyolu'))
async def handle_lifepath_command(event):
    dogum_tarihi_full = event.raw_text.split('/hayatyolu')
    dogum_tarihi = dogum_tarihi_full[1].strip()
    dogum_tarihi = datetime.strptime(dogum_tarihi, '%d.%m.%Y')

    
    try:
        hayat_sayisi = birthdate_to_life_path(dogum_tarihi)
        
        content = life_path_to_content(hayat_sayisi,Path('data/'))
        
        if content:
            await event.respond(f"Hayat Sayısı: {hayat_sayisi}\n\n{content}", parse_mode='md')
        else:
            await event.respond(f"Hayat sayısı dosyası '{hayat_sayisi}.md' bulunamadı.")
    
    except Exception as e:
        await event.respond(f"Bir hata oluştu: {str(e)}")

client.start()
print("Bot started...")
client.run_until_disconnected()
