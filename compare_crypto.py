import sys
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import alpha_vantage

def compare(currency_1, currency_2, interval='MONTHLY'):
    dates_1, prices_1 = alpha_vantage.get_crypto_price_history(currency_1, interval)
    dates_2, prices_2 = alpha_vantage.get_crypto_price_history(currency_2, interval)

    data_1 = dict(zip(dates_1, prices_1))
    data_2 = dict(zip(dates_2, prices_2))

    data_1 = { k:v for (k,v) in data_1.items() if k in data_2.keys() }
    data_2 = { k:v for (k,v) in data_2.items() if k in data_1.keys() }

    data_1 = adjust_values(data_1)
    data_2 = adjust_values(data_2)

    plt.plot(data_1.keys(), data_1.values(), label=currency_1)
    plt.plot(data_2.keys(), data_2.values(), label=currency_2)

    plt.xlabel('Date')
    plt.ylabel('Price (USD)')

    plt.title('%s and %s price history (adjusted)' % (currency_1, currency_2))
    plt.legend()
    plt.show()

def adjust_values(data, start=100.0):
    scale_factor = None

    for k, v in sorted(data.items()):
        if scale_factor == None:
            scale_factor = v / start

        data[k] = v / scale_factor

    return data

if len(sys.argv) > 3:
    compare(sys.argv[1], sys.argv[2], sys.argv[3])
else:
    compare(sys.argv[1], sys.argv[2])
