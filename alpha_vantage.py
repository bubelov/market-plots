from dotenv import load_dotenv
from os.path import join, dirname
from dateutil import parser
from enum import Enum
from typing import List
import os
import urllib.request as url_request
import json
from dataclasses import dataclass
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

API_KEY = os.getenv('ALPHA_VANTAGE_KEY')
REQUEST_TIMEOUT_SECONDS = 20


class Interval(Enum):
    DAILY = 'DAILY'
    WEEKLY = 'WEEKLY'
    MONTHLY = 'MONTHLY'


@dataclass
class AssetPrice:
    date: str
    price: float


def get_stock_returns_history(symbol: str,
                              interval: Interval) -> [float]:
    price_history = get_stock_price_history(symbol, interval, adjusted=True)

    returns: [float] = []
    prev_price = None

    for item in price_history:
        if prev_price != None:
            returns.append((item.price - prev_price) / prev_price)

        prev_price = item.price

    return returns


def get_stock_price_history(symbol: str,
                            interval: Interval,
                            adjusted=False) -> List[AssetPrice]:
    url = url_for_function('TIME_SERIES_%s' % interval.value)

    if adjusted == True:
        url += '_ADJUSTED'

    url += '&apikey=%s' % API_KEY
    url += '&symbol=%s' % symbol
    url += '&outputsize=full'

    response = url_request.urlopen(url, timeout=REQUEST_TIMEOUT_SECONDS)
    data = json.load(response)
    prices_json = data[list(data.keys())[1]]

    field_name = '4. close' if adjusted == False else '5. adjusted close'

    prices: List[AssetPrice] = []

    for k, v in sorted(prices_json.items()):
        prices.append(AssetPrice(date=parser.parse(k),
                                 price=float(v[field_name])))

    return prices


def get_crypto_returns_history(currency: str, interval: Interval):
    _, prices = get_crypto_price_history(currency, interval)

    returns = []
    prev_price = None

    for price in prices:
        if prev_price != None:
            returns.append(((price / prev_price) - 1.0) * 100.0)

        prev_price = price

    return returns


def get_crypto_price_history(currency: str, interval: Interval):
    url = url_for_function('DIGITAL_CURRENCY_%s' % interval.value)
    url += '&apikey=%s' % API_KEY
    url += '&symbol=%s' % currency
    url += '&market=%s' % 'USD'

    response = url_request.urlopen(url, timeout=REQUEST_TIMEOUT_SECONDS)
    data = json.load(response)
    _, dates_key = data.keys()
    dates_data = data[dates_key]

    dates = []
    prices = []

    for k, v in sorted(dates_data.items()):
        dates.append(parser.parse(k))
        prices.append(float(v['4a. close (USD)']))

    return (dates, prices)


def url_for_function(function: str):
    return f'https://www.alphavantage.co/query?function={function}'
