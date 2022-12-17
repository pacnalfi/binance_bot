# Telegram Constants
TG_APP_API_ID = 0                                 # Api ID of Telegramm App
TG_APP_API_HASH = ""    # Api Hash of Telegram App
TG_SESSION_FILE_NAME = "TG-Binance-Bot-Session-File"    # название файла сессии, при изменении придётся заново аутентифицироваться
CHANNEL = 'https://t.me/'               # Telegram channel link

# Binance Constants
BINANCE_API_KEY = ""        # Binance Api key
BINANCE_SECRET_KEY = ""     # Binance Secret key
BINANCE_API_URL = ""                                      # Binance ссылка на api, пока что стоит тестовая

# Order Buy Constants
MAIN_ASSET = "BTC"          # Main currency
ONE_ORDER_AMOUNT = 0.0001   # MAIN_ASSET amount value, (budget)
RECV_WINDOW_CONSTANT = 5000 # сколько максимум миллисекунд может пройти с момента отправки запроса до его принятия на сервере бинанса,
                            # прежде чем запрос может считаться неактуальным
                            # то есть, если запрос шёл дольше указанных миллисекунд, он аннулируется и не исполняется

# Logs Constants
_LOG_FILE = "{0}-technical-log.log" # название файла с тех.логами "сегодняшняя_дата-technical-log.log"
_TRADE_FILE = "{0}-trade-log.log"   # название файла с трейд.логами "сегодняшняя_дата-trade-log.log"

# Stop_Phrases Constants
STOP_PHRASES_AFTER = [
    "The coin we have picked to pump today is :  #",
    "The coin we have picked to pump today is :  $",
    "The coin we have picked to pump today is :  ",
    "/trade/"
]

# Available prefixes Constants
SIGNS_PREFIXES = [
    "#",
    "@",
    "$"
]
