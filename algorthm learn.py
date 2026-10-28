import aiohttp
import asyncio
from datetime import datetime

BOT_TOKEN = '8324582205:AAGIjLX_1oU81MBCo6SyaEGY6Z-2T6K7PxQ'
API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/'


async def send_message(payload, session, now):
    URL_SEND = f'{API_URL}sendMessage'
    if payload['text'] == '/time':
        payload['text'] = f'{now.strftime("%d.%m.%Y, время: %H:%M:%S")}'
    elif payload['text'] == '/start':
        payload['text'] = 'Я тут!'
    async with session.post(URL_SEND, params=payload):
        pass


async def echo_bot():
    offset = 0

    print('бот запущен')

    async with aiohttp.ClientSession() as session:
        while True:
            tasks = []
            URL_UPDATE = f'{API_URL}getUpdates'
            params = {'offset': offset + 1}

            async with session.get(URL_UPDATE, params=params) as response:
                updates = await response.json()
            if updates['result']:
                for i in updates['result']:
                    now = datetime.now()
                    if 'text' in i['message']:
                        offset = i['update_id']
                        chat_id = i['message']['from']['id']
                        text = i['message']['text']
                        payload = {'chat_id': chat_id,
                                   'text': text
                                   }
                        print(f'id: {chat_id} написал: \'{text}\', дата: {now.strftime("%d.%m.%Y, время: %H:%M:%S")}')

                        task = send_message(payload, session, now)
                        tasks.append(task)

                    else:
                        offset = i['update_id']
                        chat_id = i['message']['from']['id']
                        print(
                            f'id:{chat_id} отправил гифку, фото или картинку, дата: {now.strftime("%d.%m.%Y, время: %H:%M:%S")}')
            if tasks:
                await asyncio.gather(*tasks)


asyncio.run(echo_bot())
