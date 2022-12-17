import configparser
import json
import config as CF
from signs_db import SIGNS
import logging
from datetime import date
from telethon.errors import SessionPasswordNeededError
from telethon import TelegramClient, events, sync
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (PeerChannel)
from binance_bot import Binance_Manager
import pyfiglet



# Функция, в которую поступает текс, из которого нужно вытащить знак валюты.
# Возвращает "NOTFOUND", если знаков не было обнаружено, иначе строку со знаком (пример: "BTC")
def parse_tokens(text):
    logging.info(f"Пришёл текст\n {text}")
    # первый метод: поиск всех возможных стоп-фраз, перечисленных в config.py, после которых сразу идёт название монеты
    # То есть пример: <фраза>МОНЕТА, то есть во фразе пробелы тоже учитываются, это прямо строгий отбор
    for cur_stop_phrase in CF.STOP_PHRASES_AFTER:

        if cur_stop_phrase in text:
            coin = ""
            idx = text.find(cur_stop_phrase) + len(cur_stop_phrase)

            while idx < len(text) and text[idx].isalpha():
                coin += text[idx]
                idx += 1
            
            return coin
    # второй метод: поиск всех возможных знаков валют в тексте (то есть перебор по всей базе SIGNS в signs_db.py)
    # база обновляется из самого Binance, для обновления просто запустите misc.py, он сам сотрёт прошлую базу и запишет новую
    words = text.split()
    for sign in SIGNS:

        if sign in words:
            return sign

        else:
            for pref in CF.SIGNS_PREFIXES:
                if pref+sign in words:
                    return sign
    
    return "NOTFOUND"
    
# Основная функция
def main():
    logging.basicConfig(
        filename=CF._LOG_FILE.format(str(date.today())), 
        encoding="utf-8", 
        level=logging.NOTSET,
        format='%(asctime)s [%(levelname)s] src:%(filename)s func:%(funcName)s() ln:%(lineno)s msg: %(message)s'
        )
    logging.info("Main запустился.")
    print("Main запустился.")

    logging.info("Создаю Telegram_Client.")
    print("Создаю Telegram_Client.")
    telegram_client = TelegramClient(
        CF.TG_SESSION_FILE_NAME, 
        CF.TG_APP_API_ID, 
        CF.TG_APP_API_HASH
        )

    logging.info("Создаю логгер для трейда.")
    print("Создаю логгер для трейда.")
    trade_file_handler = logging.FileHandler(CF._TRADE_FILE.format(str(date.today())), encoding="utf-8")
    trade_file_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] msg: %(message)s'))
    trade_logger = logging.getLogger(name="BotLog")
    trade_logger.setLevel(logging.NOTSET)
    trade_logger.addHandler(trade_file_handler)

    logging.info("Создаю Binance_Manager.")
    print("Создаю Binance_Manager.")
    BN_MANAGER = Binance_Manager(trade_logger)

    trade_logger.info("Начинаю сессию.")
    print("Начинаю сессию.")
    trade_logger.info("Доступные пары для трейдинга:")
    print("Available pairs for trading:")
    all_pairs = BN_MANAGER.get_all_pairs()
    

    for idx in range(len(all_pairs)):
        print(all_pairs[idx], end=" ")

        if idx%2:
            print()

    if len(all_pairs) % 2:
        print()
        
    result = pyfiglet.figlet_format("Kaan_Bot")
    print(result)

    @telegram_client.on(events.NewMessage(chats=CF.CHANNEL))
    async def NewMessageListener(event):
        logging.info("Новый пост. Получаю текст.")
        text = str(event.message.message)
        found = parse_tokens(text)

        if found == "NOTFOUND":
            logging.info("Не нашёл знака валюты.")

        else:
            logging.info(f"Нашёл валюту {found}")
            logging.info(f"Отправляю запрос менеджеру BN_MANAGER: {found}")
            BN_MANAGER.make_order(found)

    with telegram_client:
        telegram_client.run_until_disconnected()


if __name__ == "__main__":

    main()
