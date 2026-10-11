import requests


API_URL = 'https://api.telegram.org/bot'
BOT_TOKEN = '8942859997:AAFPBtL5VRW1qgG1Ps_M4zrtc8MCztA3NYc'

offset=-2
while True:
    update=requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset+1}').json()

    if update['result']:
        offset=update['result'][0]['update_id']
        chat_id=update['result'][0]['message']['from']['id']
        text=update['result'][0]['message']['text']
        requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={text}')
