import sys
from dateutil import parser
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import alpha_vantage

def show_price_history(symbol_1, symbol_2, interval="MONTHLY"):
    symbol_1_x_values, symbol_1_y_values = get_price_history_values(symbol_1, interval)
    symbol_2_x_values, symbol_2_y_values = get_price_history_values(symbol_2, interval)

    if len(symbol_2_x_values) > len(symbol_1_x_values):
        symbol_2_x_values = symbol_2_x_values[:-(len(symbol_2_x_values) - len(symbol_1_x_values))]
        symbol_2_y_values = symbol_2_y_values[:-(len(symbol_2_y_values) - len(symbol_1_y_values))]

    plt.plot(symbol_1_x_values, adjust_relative(symbol_1_y_values), label=symbol_1)
    plt.plot(symbol_2_x_values, adjust_relative(symbol_2_y_values), label=symbol_2)

    plt.xlabel('Date')
    plt.ylabel('Price (USD)')

    plt.title('%s vs %s price history' % (symbol_1, symbol_2))
    plt.legend()
    plt.show()

def get_price_history_values(symbol, interval):
    data = alpha_vantage.get_stock_price_history(symbol, interval + "_ADJUSTED")
    meta_key, dates_key = data.keys()
    dates_data = data[dates_key]

    x_values = []
    y_values = []

    for k, v in dates_data.items():
        x_values.append(parser.parse(k))
        y_values.append(float(v['5. adjusted close']))

    return (x_values, y_values)

def adjust_relative(values, pivot=100.0):
    factor = values[-1] / pivot
    return [v / factor for v in values]

if len(sys.argv) > 3:
    show_price_history(sys.argv[1], sys.argv[2], sys.argv[3])
else:
    show_price_history(sys.argv[1], sys.argv[2])
