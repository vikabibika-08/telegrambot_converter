import requests
import json
from config import keys, API_KEY


class APIException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def convert(quote:str, base:str, amount:str):
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

        link = f'http://api.exchangeratesapi.io/v1/latest?access_key={API_KEY}'
        r = requests.get(f'{link}&base={quote_ticker}&symbols={base_ticker}')
        total_base = round(float(amount) * float(json.loads(r.content)['rates'][keys[base]]),2)

        return total_base

