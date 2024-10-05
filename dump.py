#!/usr/bin/env python3

# This script is modified from https://gist.github.com/avivace/4eb547067e364d416c074b68502e0136

import time, os

from telethon import TelegramClient, events, sync
from telethon.tl.types import InputChannel, PeerChannel
from telethon.tl.types import Channel

from dotenv import load_dotenv

load_dotenv()

# Get your own api_id and
# api_hash from https://my.telegram.org, under API Development.

GROUP_CHAT_ID=int(os.getenv('GROUP_CHAT_ID'))
API_ID=os.getenv('API_ID')
API_HASH=os.getenv('API_HASH')

client = TelegramClient('telegram_session', API_ID, API_HASH)
client.start()

group = client.get_entity(PeerChannel(GROUP_CHAT_ID))

file = open('dump.json','w')
message_id = 0
media_id = 0
for event in client.iter_admin_log(group):
    if event.deleted_message:
        print(f'dump<message={message_id},event.old.id={event.old.id},event.old.date={event.old.date},event.action.message.id={event.action.message.id}>')
        file.write(event.old.to_json() + ',') 
        message_id += 1
        if event.old.media:
            media_id += 1
            client.download_media(event.old.media, str(event.old.id))
            print(f'dump<media={media_id}>')
        time.sleep(0.1)
