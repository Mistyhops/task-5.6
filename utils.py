import requests
import json
from config import keys


class ConvertionException(Exception):
    pass


class CurrConverter:
    @staticmethod
    def amount_type(amount):
        try:
            amount = float(amount)
            if int(amount) != float(amount):
                amount = float(amount)
            else:
                amount = int(amount)
        except ValueError:
            raise ConvertionException('Не удается обработать количество. Введите /help для получения подсказки.')
        return amount


    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Нельзя выбрать одинаковые валюты {quote} для конвертации.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}.')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException('Не удается обработать количество. Введите /help для получения подсказки.')

        r = requests.get(f'https://api.exchangeratesapi.io/latest?symbols={base_ticker}&base={quote_ticker}')
        total_base = json.loads(r.content)['rates'][base_ticker]

        return total_base
