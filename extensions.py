import requests
import json

keys = {
    'Рубль': "RUB",
    'Евро': "EUR",
    'Доллар': "USD",
}

class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str): #message: telebot.types.Message,        
        
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}')
        
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')
        
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')
        
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')
        
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        
        return json.loads(r.content)[keys[base]]
