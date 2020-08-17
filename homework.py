import time

import requests
from twilio.rest import Client
from dotenv import load_dotenv
import os
load_dotenv()


def get_status(user_id):
    params = {
        'user_ids': user_id,
        'fields': 'online',
        'v': 5.92,
        'access_token': os.getenv('access_token')
    }
    url = 'https://api.vk.com/method/users.get'
    r = requests.post(url, params=params)
    for data in r.json()['response']:
        return data['online']


def sms_sender(sms_text):
    account_sid = os.getenv('account_sid')
    auth_token = os.getenv('auth_token')
    NUMBER_FROM = os.getenv('phone_number_from')
    NUMBER_TO = os.getenv('phone_number_to')
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=sms_text,
        from_=NUMBER_FROM,
        to=NUMBER_TO
    )
    print(message.sid)
    return message.sid


if __name__ == "__main__":
    vk_id = input("Введите id ")
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
