import sys
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import alpha_vantage

def compare_stocks(symbol_1, symbol_2, interval="MONTHLY"):
    dates_1, prices_1 = alpha_vantage.get_stock_price_history(symbol_1, interval, adjusted=True)
    dates_2, prices_2 = alpha_vantage.get_stock_price_history(symbol_2, interval, adjusted=True)

    data_1 = dict(zip(dates_1, prices_1))
    data_2 = dict(zip(dates_2, prices_2))

    data_1 = { k:v for (k,v) in data_1.items() if k in data_2.keys() }
    data_2 = { k:v for (k,v) in data_2.items() if k in data_1.keys() }

    data_1 = adjust_values(data_1)
    data_2 = adjust_values(data_2)

    plt.plot(data_1.keys(), data_1.values(), label=symbol_1)
    plt.plot(data_2.keys(), data_2.values(), label=symbol_2)

    plt.xlabel('Date')
    plt.ylabel('Price (USD)')

    plt.title('%s and %s price history (adjusted)' % (symbol_1, symbol_2))
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
    compare_stocks(sys.argv[1], sys.argv[2], sys.argv[3])
else:
    compare_stocks(sys.argv[1], sys.argv[2])
