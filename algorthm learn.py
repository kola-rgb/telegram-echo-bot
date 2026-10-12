import aiohttp
import asyncio
from datetime import datetime

BOT_TOKEN = '8942859997:AAFPBtL5VRW1qgG1Ps_M4zrtc8MCztA3NYc'
API_URL = 'https://api.telegram.org/bot8942859997:AAFPBtL5VRW1qgG1Ps_M4zrtc8MCztA3NYc/'


async def send_message(offset, chat_id, session, text):
    async with session.post(f'{API_URL}sendMessage?chat_id={chat_id}&text={text}'):
        pass


async def echo_bot():
    offset = -2

    print('бот запущен')

    async with aiohttp.ClientSession() as session:
        while True:
            tasks = []
            now=datetime.now()
            async with session.get(f'{API_URL}getUpdates?offset={offset + 1}') as response:
                updates = await response.json()
            if updates['result']:
                if 'text' in updates['result'][0]['message']:
                    offset = updates['result'][0]['update_id']
                    chat_id = updates['result'][0]['message']['from']['id']
                    text = updates['result'][0]['message']['text']
                    print(f'id: {chat_id} написал: \'{text}\', дата: {now.strftime("%d.%m.%Y, время: %H:%M:%S")}')
                    task = send_message(offset, chat_id, session, text)
                    tasks.append(task)
                else:
                    offset = updates['result'][0]['update_id']
                    chat_id = updates['result'][0]['message']['from']['id']
                    print(f'id:{chat_id} отправил гифку, фото или картинку, дата: {now.strftime("%d.%m.%Y, время: %H:%M:%S")}')
            if tasks:
                await asyncio.gather(*tasks)


asyncio.run(echo_bot())
