import urllib.request as url_request
import json

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

API_KEY = 'WVK0W8WGQRYMAYXS'
REQUEST_TIMEOUT_SECONDS = 20

def get_stock_price_history(symbol, interval):
    url = url_for_function('TIME_SERIES_%s' % interval)
    url += '&apikey=%s' % API_KEY
    url += '&symbol=%s' % symbol
    url += '&outputsize=full'

    if interval == 'INTRADAY':
        url += '&interval=5min'

    response = url_request.urlopen(url, timeout=REQUEST_TIMEOUT_SECONDS)
    return json.load(response)

def get_crypto_price_history(base_currency, quote_currency, interval):
    url = url_for_function('DIGITAL_CURRENCY_%s' % interval)
    url += '&apikey=%s' % API_KEY
    url += '&symbol=%s' % base_currency
    url += '&market=%s' % quote_currency

    response = url_request.urlopen(url, timeout=REQUEST_TIMEOUT_SECONDS)
    return json.load(response)

def url_for_function(function):
    return 'https://www.alphavantage.co/query?function=%s' % function
