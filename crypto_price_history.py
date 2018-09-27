import sys
from dateutil import parser
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import alpha_vantage

def show_price_history(base_currency, interval):
    data = alpha_vantage.get_crypto_price_history(base_currency, 'USD', interval)
    meta_key, dates_key = data
    dates_data = data[dates_key]

    x_values = []
    y_values = []

    for k, v in dates_data.items():
        x_values.append(parser.parse(k))
        y_values.append(float(v['4a. close (USD)']))

    plt.title('%s price history' % base_currency)
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.plot(x_values, y_values)
    plt.show()

show_price_history(sys.argv[1], sys.argv[2])
