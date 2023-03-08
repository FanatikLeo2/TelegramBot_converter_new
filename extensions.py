import requests
import json
from config import keys, headers


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'Невозможно конвертировать одинаковые валюты ({base})')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту ({quote})')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту ({base})')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество ({amount})')

#       r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
#       total_base = round((json.loads(r.content)[keys[base]] * float(amount)), 2)

        r = requests.get(f"https://api.apilayer.com/exchangerates_data/latest?symbols={base_ticker}&base={quote_ticker}", headers=headers)
        total_base = round(json.loads(r.content)['rates'][base_ticker] * amount, 2)

        return total_base
