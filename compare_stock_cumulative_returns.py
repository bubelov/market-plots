import sys
from dateutil import parser
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import alpha_vantage

def show_price_history(symbol_1, symbol_2, interval="MONTHLY"):
    values_1 = get_price_history_values(symbol_1, interval)
    values_2 = get_price_history_values(symbol_2, interval)

    values_1 = { k:v for (k,v) in values_1.items() if k in values_2.keys() }
    values_2 = { k:v for (k,v) in values_2.items() if k in values_1.keys() }

    values_1 = adjust_values(values_1)
    values_2 = adjust_values(values_2)

    plt.plot(values_1.keys(), values_1.values(), label=symbol_1)
    plt.plot(values_2.keys(), values_2.values(), label=symbol_2)

    plt.xlabel('Date')
    plt.ylabel('Price (USD)')

    plt.title('%s vs %s price history' % (symbol_1, symbol_2))
    plt.legend()
    plt.show()

def get_price_history_values(symbol, interval):
    data = None
    dates_data = None

    try:
        data = alpha_vantage.get_stock_price_history(symbol, interval + "_ADJUSTED")
        meta_key, dates_key = data.keys()
        dates_data = data[dates_key]
    except:
        print("Cannot parse response: %s" % data)

    result = {}

    for k, v in sorted(dates_data.items()):
        result[parser.parse(k)] = float(v['5. adjusted close'])

    return result

def adjust_values(map, pivot=100.0):
    scale_factor = None

    for k, v in sorted(map.items()):
        if scale_factor == None:
            scale_factor = v / pivot

        map[k] = v / scale_factor

    return map

if len(sys.argv) > 3:
    show_price_history(sys.argv[1], sys.argv[2], sys.argv[3])
else:
    show_price_history(sys.argv[1], sys.argv[2])
