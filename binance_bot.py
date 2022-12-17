import config as CF
import logging
from binance.client import Client
from binance.exceptions import *
from datetime import date

class Binance_Manager:

    def __init__(self, trade_logger_instance):
        self.api_key = CF.BINANCE_API_KEY
        self.api_secret = CF.BINANCE_SECRET_KEY
        self.api_binance_url = CF.BINANCE_API_URL
        self.main_asset = CF.MAIN_ASSET
        self.client = Client(self.api_key, self.api_secret)
        self.client.API_URL = self.api_binance_url
        self.trade_logger = trade_logger_instance
    
    def get_all_pairs(self):
        res = self.client.get_all_tickers()
        res = [ticker['symbol'] for ticker in res]
        res.sort()
        return res
    
    def make_order(self, add_asset):
        if add_asset == CF.MAIN_ASSET:
            logging.warning(f"Пара {add_asset+CF.MAIN_ASSET} не существует")
            self.trade_logger.info(f"Пара {add_asset+CF.MAIN_ASSET} не существует")
            print(f"Пара {add_asset+CF.MAIN_ASSET} не существует")
            return
        self.trade_logger.info(f"Пытаюсь сделать ордер на пару {add_asset+self.main_asset}.")
        symbol_info = self.client.get_symbol_info(add_asset+self.main_asset)
        logging.info(f"Данные о паре:")
        logging.info(symbol_info)
        if symbol_info['status'] != "TRADING":
            self.trade_logger.info(f"This pair {add_asset + self.main_asset} is not available for trading.")
            return
        if 'MARKET' not in symbol_info['orderTypes']:
            self.trade_logger.info(f"Market не доступен для пары {add_asset+self.main_asset}")
            return
        order_amount = f"%.{symbol_info['quotePrecision']}f" % CF.ONE_ORDER_AMOUNT
        try:
            buy_order = self.client.order_market_buy(
                symbol = add_asset + self.main_asset,
                side = "BUY",
                type = "MARKET",
                quoteOrderQty = order_amount,
                recvWindow = CF.RECV_WINDOW_CONSTANT
            )
            logging.info(f"Order placed: {repr(buy_order)}")
            print(f"Placed BUY order on the Market: Pair = {add_asset+self.main_asset} amount = {str(CF.ONE_ORDER_AMOUNT)+' '+self.main_asset}")
            self.trade_logger.info(f"Placed BUY order on the Market: Pair = {add_asset+self.main_asset} amount = {str(CF.ONE_ORDER_AMOUNT)+' '+self.main_asset}")
            print("FILLS")
            self.trade_logger.info("FILLS")
            for fill in buy_order['fills']:
                print(f"Total: {fill['price']}\nAmount: {fill['qty']}\nCommission: {fill['commission']}\nCommission Asset: {fill['commissionAsset']}\nTrade Id: {fill['tradeId']}")
                self.trade_logger.info(f"Total: {fill['price']}\nAmount: {fill['qty']}\nCommission: {fill['commission']}\nCommission Asset: {fill['commissionAsset']}\nTrade Id: {fill['tradeId']}")
        except BinanceAPIException as e:
            logging.warning(e)
            self.trade_logger.warning("ERROR", e)
            print("ERROR, ПОСМОТРИТЕ ТЕХНИЧЕСКИЕ ЛОГИ", e)
        except BinanceOrderException as e:
            logging.warning(e)
            self.trade_logger.warning("ОШИБКА", e)
            print("ERROR, ПОСМОТРИТЕ ТЕХНИЧЕСКИЕ ЛОГИ", e)
        except Exception as err:
            logging.warning(err)
            self.trade_logger.warning("ОШИБКА", err)
            print("ERROR, ПОСМОТРИТЕ ТЕХНИЧЕСКИЕ ЛОГИ", err)
