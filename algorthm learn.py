import aiohttp
import asyncio

from requests import session

BOT_TOKEN = '8942859997:AAFPBtL5VRW1qgG1Ps_M4zrtc8MCztA3NYc'
API_URL = 'https://api.telegram.org/bot8942859997:AAFPBtL5VRW1qgG1Ps_M4zrtc8MCztA3NYc/'


async def send_message(offset, chat_id, session,text):
    async with session.post(f'{API_URL}sendMessage?chat_id={chat_id}&text={text}'):
        pass


async def main():
    offset = -2
    async with aiohttp.ClientSession() as session:
        while True:
            tasks = []
            async with session.get(f'{API_URL}getUpdates?offset={offset + 1}') as response:
                updates = await response.json()
            if updates['result']:
                offset = updates['result'][0]['update_id']
                chat_id = updates['result'][0]['message']['from']['id']
                text = updates['result'][0]['message']['text']
                task = send_message(offset, chat_id, session,text)
                tasks.append(task)
            if tasks:
                await asyncio.gather(*tasks)

asyncio.run(main())