import aiohttp
import asyncio
from datetime import datetime

BOT_TOKEN = 'PAST'
API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/'


async def send_message(chat_id, session, text):
    async with session.post(f'{API_URL}sendMessage?chat_id={chat_id}&text={text}'):
        pass


async def start_message(chat_id, session):
    async with session.post(f'{API_URL}sendMessage?chat_id={chat_id}&text=Я тут!'):
        pass


async def send_time(chat_id, session, now):
    async with session.post(f'{API_URL}sendMessage?chat_id={chat_id}&text={now.strftime("%d.%m.%Y, время: %H:%M:%S")}'):
        pass


async def echo_bot():
    offset = -2

    print('бот запущен')

    async with aiohttp.ClientSession() as session:
        while True:
            tasks = []
            async with session.get(f'{API_URL}getUpdates?offset={offset + 1}') as response:
                updates = await response.json()
            if updates['result']:
                for i in updates['result']:
                    now = datetime.now()
                    if 'text' in i['message']:
                        offset = i['update_id']
                        chat_id = i['message']['from']['id']
                        text = i['message']['text']
                        print(f'id: {chat_id} написал: \'{text}\', дата: {now.strftime("%d.%m.%Y, время: %H:%M:%S")}')

                        if text == '/time':
                            task = send_time(chat_id, session, now)
                            tasks.append(task)
                        elif text == '/start':
                            task = start_message(chat_id, session)
                            tasks.append(task)
                        else:
                            task = send_message(chat_id, session, text)
                            tasks.append(task)

                    else:
                        offset = i['update_id']
                        chat_id = i['message']['from']['id']
                        print(
                            f'id:{chat_id} отправил гифку, фото или картинку, дата: {now.strftime("%d.%m.%Y, время: %H:%M:%S")}')
            if tasks:
                await asyncio.gather(*tasks)


asyncio.run(echo_bot())
