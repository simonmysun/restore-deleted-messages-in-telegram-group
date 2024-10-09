#!/usr/bin/env python3

# This script is modified from the commments of https://gist.github.com/avivace/4eb547067e364d416c074b68502e0136

import json
import time
import os
import sys
import glob
from telethon import TelegramClient
from telethon.tl.types import PeerChannel
from datetime import datetime
import asyncio
from dotenv import load_dotenv

load_dotenv()

GROUP_CHAT_ID=int(os.getenv('GROUP_CHAT_ID'))
API_ID=os.getenv('API_ID')
API_HASH=os.getenv('API_HASH')

async def main():
  with open('dump.json', 'r') as file:
    content = json.load(file)
    # sort by date:
    content = sorted(content, key=lambda x: x['date'])

    client = TelegramClient('telegram_session', API_ID, API_HASH)
    await client.start()

    group = await client.get_entity(PeerChannel(GROUP_CHAT_ID))

    for msg in content:
      message_id = msg['id']
      message = msg.get('message', '')
      has_media = msg.get('media', None) is not None
      has_message = message != ''
      date = datetime.fromisoformat(msg['date']).strftime('%Y-%m-%dT%H:%M:%S')

      from_user = msg['from_id']['user_id']
      reply_to = msg['reply_to']['reply_to_msg_id'] if msg.get('reply_to') is not None else ''
      fwd_from = ''
      if msg.get('fwd_from') is not None:
        if msg['fwd_from'].get('from_id') is not None:
          fwd_from = msg['fwd_from']['from_id']
          if fwd_from.get('channel_id') is not None:
            fwd_from = f'{{channel_id={fwd_from['channel_id']}}}'
          else:
            fwd_from = f'{{user_id={fwd_from['user_id']}}}'
      via_bot = msg.get('via_bot_id')
      via_bot = '' if via_bot is None else via_bot

      message = f'id={message_id},date={date},msg="{message}",from_user={from_user},reply_to={reply_to},fwd_from={fwd_from},via_bot={via_bot}'
      print(message)

      if has_media:
        if msg['media']['_'] == 'MessageMediaDocument':
          file_names = glob.glob(f'{message_id}.*')
          for file_name in file_names:
            print(f'Sending Media: {file_name}')
            try:
              await client.send_file(entity=group, file=file_name, caption=message, silent=True, force_document=True)
            except Exception as e:
              print(f'Error sending file {file_name}: {str(e)}', file=sys.stderr)
        elif msg['media']['_'] == 'MessageMediaPhoto':
          file_names = glob.glob(f'{message_id}.*')
          for file_name in file_names:
            print(f'Sending Media: {file_name}')
            try:
              await client.send_file(entity=group, file=file_name, caption=message, silent=True, force_document=False)
            except Exception as e:
              print(f'Error sending media {file_name}: {str(e)}', file=sys.stderr)
      else:
        print(f'Sending Message: {message}')
        try:
          await client.send_message(entity=group, message=message, silent=True)
        except Exception as e:
          print(f'Error sending message: {str(e)}', file=sys.stderr)

      # sleep to avoid rate limiting, you may experiment with reducing this time:
      time.sleep(2)

asyncio.run(main())
