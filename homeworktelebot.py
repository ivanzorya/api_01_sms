import logging
import os
import time

import requests
import telegram
from dotenv import load_dotenv

load_dotenv()


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
URL = 'https://praktikum.yandex.ru/api/user_api/homework_statuses/'
# PROXY = telegram.utils.request.Request(proxy_url='socks5://68.183.69.147:1080')
bot = telegram.Bot(token=TELEGRAM_TOKEN) # request=PROXY)


def parse_homework_status(homework):
    try:
        homework_name = homework.get('homework_name')
        if homework_name is None:
            raise Exception('Not correct name')
        homework_status = homework.get('status')
        if homework_status not in ('rejected', 'approved'):
            raise Exception('Not correct status')
        if homework_status == 'rejected':
            verdict = 'К сожалению в работе нашлись ошибки.'
        else:
            verdict = 'Ревьюеру всё понравилось, можно приступать к следующему уроку.'
        return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'
    except Exception as e:
        logging.exception(f'Bad value. {e}')


def get_homework_statuses(current_timestamp):
    headers = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
    if current_timestamp is None:
        current_timestamp = int(time.time())
    params = {'from_date': current_timestamp}
    try:
        homework_statuses = requests.get(URL, params=params, headers=headers)
        return homework_statuses.json()
    except Exception as e:
        logging.exception(f'Request raised. Error: {e}')


def send_message(message):
    return bot.send_message(chat_id=CHAT_ID, text=message)


def main():
    current_timestamp = int(time.time())

    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework.get('homeworks'):
                send_message(parse_homework_status(new_homework.get('homeworks')[0]))
            current_timestamp = new_homework.get('current_date')
            time.sleep(300)

        except Exception as e:
            print(f'Бот упал с ошибкой: {e}')
            time.sleep(5)
            continue


if __name__ == '__main__':
    main()
