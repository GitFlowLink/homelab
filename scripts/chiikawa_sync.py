from telethon import TelegramClient
from telethon.tl.types import DocumentAttributeVideo
import asyncio
import os
import json

# Берём из переменных окружения (.env файл или systemd)
api_id = int(os.getenv('TG_API_ID'))
api_hash = os.getenv('TG_API_HASH')
channel = os.getenv('TG_CHANNEL', 'Chiikawarussub')
download_path = os.getenv('DOWNLOAD_PATH', '/mnt/media/anime/Chiikawa (2022)/Season 01')
state_file = os.getenv('STATE_FILE', '/root/chiikawa_state.json')

def load_last_id():
    if os.path.exists(state_file):
        with open(state_file) as f:
            return json.load(f).get('last_id', 0)
    return 0

def save_last_id(last_id):
    with open(state_file, 'w') as f:
        json.dump({'last_id': last_id}, f)

def get_next_episode():
    files = [f for f in os.listdir(download_path) if f.endswith('.mp4')]
    return len(files) + 1

async def main():
    last_id = load_last_id()
    new_last_id = last_id
    async with TelegramClient('session', api_id, api_hash) as client:
        async for message in client.iter_messages(channel, min_id=last_id, reverse=True):
            if message.video or message.document:
                duration = 0
                if message.document:
                    for attr in message.document.attributes:
                        if isinstance(attr, DocumentAttributeVideo):
                            duration = attr.duration
                elif message.video:
                    duration = getattr(message.video, 'duration', 0)
                if duration > 45:
                    ep = get_next_episode()
                    filename = f'{download_path}/Chiikawa S01E{ep:03d}.mp4'
                    print(f'Скачиваю эпизод {ep} (id={message.id}, {duration}s)')
                    await message.download_media(filename)
            if message.id > new_last_id:
                new_last_id = message.id
    save_last_id(new_last_id)
    print('Готово')

asyncio.run(main())
