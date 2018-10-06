import urllib.request as url_request
import json
from dateutil import parser
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

API_KEY = 'WVK0W8WGQRYMAYXS'
REQUEST_TIMEOUT_SECONDS = 20

def get_stock_returns_history(symbol, interval):
    dates, prices = get_stock_price_history(symbol, interval, adjusted=True)

    returns = []
    prev_price = None

    for price in prices:
        if prev_price != None:
            returns.append(((price / prev_price) - 1.0) * 100.0)

        prev_price = price

    return returns

def get_stock_price_history(symbol, interval, adjusted=False):
    url = url_for_function('TIME_SERIES_%s' % interval)

    if adjusted == True:
        url += '_ADJUSTED'

    url += '&apikey=%s' % API_KEY
    url += '&symbol=%s' % symbol
    url += '&outputsize=full'

    response = url_request.urlopen(url, timeout=REQUEST_TIMEOUT_SECONDS)
    data = json.load(response)
    meta_key, dates_key = data.keys()
    dates_data = data[dates_key]

    dates = []
    prices = []

    for k, v in dates_data.items():
        dates.append(parser.parse(k))

        if adjusted == True:
            prices.append(float(v['5. adjusted close']))
        else:
            prices.append(float(v['4. close']))

    return (dates, prices)

def get_crypto_price_history(base_currency, quote_currency, interval):
    url = url_for_function('DIGITAL_CURRENCY_%s' % interval)
    url += '&apikey=%s' % API_KEY
    url += '&symbol=%s' % base_currency
    url += '&market=%s' % quote_currency

    response = url_request.urlopen(url, timeout=REQUEST_TIMEOUT_SECONDS)
    return json.load(response)

def url_for_function(function):
    return 'https://www.alphavantage.co/query?function=%s' % function
