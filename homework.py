from http import HTTPStatus
import logging
import os
import time
import requests

import telegram
from telegram import Bot
from telegram.ext import Updater
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
    """Отправка сообщения в телеграмм."""
    bot = Bot(token=TELEGRAM_TOKEN)
    bot.send_message(TELEGRAM_CHAT_ID, message)


def get_api_answer(current_timestamp):
    """Отправка запроса к сайту Яндекс Практикум."""
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
    except Exception as error:
        logging.error(f'Ощибка при запросе к API: {error}')
    if response.status_code != HTTPStatus.OK:
        logging.error(f'API не отвечает: {response.status_code}')
        raise Exception('Ошибка ответа')
    return response.json()


def check_response(response):
    """Проверка ответа API."""
    if not isinstance(response, dict):
        raise TypeError('response is not dict')
    if response == {}:
        raise Exception('Dict is Empty')
    if 'homeworks' not in response:
        raise Exception('KeyError homeworks')
    if type(response.get('homeworks')) is not list:
        raise TypeError('homeworks is not list')
    return response['homeworks']


def parse_status(homework):
    """Информация о конкретной домашней работе, статус этой работы."""
    if homework == []:
        return None
    else:
        homework_name = homework.get('homework_name')
        homework_status = homework.get('status')

        if not homework_name:
            raise KeyError('Домашняя работа не обнаружена')

        if homework_status not in HOMEWORK_STATUSES:
            logging.Logger.debug('В ответе отсутствуют  новые статусы')
            raise logging.Logger.NoneNothing(
                'В ответе отсутствуют  новые статусы')

    verdict = HOMEWORK_STATUSES[homework_status]

    return (f'Изменился статус проверки работы "{homework_name}". {verdict}')


def check_tokens():
    """проверка доступности переменных окружения."""
    if not PRACTICUM_TOKEN:
        logging.critical('Отсутсвует токен авторизации')
    if not TELEGRAM_TOKEN:
        logging.critical('Отсутсвует токен телеграма')
    if not TELEGRAM_CHAT_ID:
        logging.critical('Отсутсвует id телерамм чата')
    else:
        return True


def main():
    """Основная логика работы бота."""
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())

    while True:
        try:
            response = get_api_answer(current_timestamp)
            homework = check_response(response)
            message = parse_status(homework)
            current_timestamp = current_timestamp
            if message is not None:
                send_message(bot, message)
            time.sleep(RETRY_TIME)

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logging.error(message)
            bot.send_message(TELEGRAM_CHAT_ID, message)
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
