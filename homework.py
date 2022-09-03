import logging
import os
from telnetlib import STATUS
import time
from urllib import response
import requests

import telegram
from telegram import Bot
from telegram.ext import Updater
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    filename='program.log',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
PAYLOAD = {'from_date': 1659511568}

HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

updater = Updater(token=TELEGRAM_TOKEN)


def send_message(bot, message):
    bot = Bot(token=TELEGRAM_TOKEN)
    message = f'Изменился статус проверки работы "{check_response.homework_name}". {check_response.verdict}'
    bot.send_message(TELEGRAM_CHAT_ID, message)


def get_api_answer(current_timestamp):
    """Отправка запроса к сайту Яндекс Практикум"""
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': 0}
    response = requests.get(ENDPOINT, headers=HEADERS, params=params).json()
    if response.status_code == 200:
        return response


def check_response(response):
    pass


def parse_status(homework):
    """Информация о конкретной домашней работе, статус этой работы."""
    # Надо  дописать тест в check_response на
    # проверку типа данных и проверка на
    # статус у меня была не в той функции.

    homework_name = homework.get('homework_name')
    homework_status = homework.get('status')

    if not homework_name:
        raise KeyError('Домашняя работа не обнаружена')

    if not homework_status in HOMEWORK_STATUSES:
        logging.Logger.debug('В ответе отсутствуют  новые статусы')
        # raise NoneNothing('В ответе отсутствуют  новые статусы')

    verdict = HOMEWORK_STATUSES[homework_status]

    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    pass


def main():
    """Основная логика работы бота."""
    homework_statuses = (requests.get(
        ENDPOINT, headers=HEADERS, params=PAYLOAD)).json()
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())

    updater.start_polling(poll_interval=RETRY_TIME)
    updater.idle()

    while True:
        try:
            response = homework_statuses

            ...

            current_timestamp = ...
            time.sleep(RETRY_TIME)

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            ...
            time.sleep(RETRY_TIME)
        else:
            ...


if __name__ == '__main__':
    main()
