import sys
from dateutil import parser
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import alpha_vantage

def show_history(currency, interval='MONTHLY'):
    dates, prices = alpha_vantage.get_crypto_price_history(currency, interval)

    plt.plot(dates, prices)

    plt.xlabel('Date')
    plt.ylabel('Price (USD)')

    plt.title('%s price history' % currency)
    plt.show()

if len(sys.argv) > 2:
    show_history(sys.argv[1], sys.argv[2])
else:
    show_history(sys.argv[1])
