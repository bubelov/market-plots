import sys
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import alpha_vantage

def show_returns_distribution(symbol, interval):
    data = alpha_vantage.get_stock_price_history(symbol, interval + '_ADJUSTED')
    meta_key, dates_key = data
    dates_data = data[dates_key]

    returns = []
    prev_key = None

    for k, v in dates_data.items():
        if prev_key != None:
            prev_period_close = float(dates_data[prev_key]['5. adjusted close'])
            current_period_close = float(v['5. adjusted close'])
            returns.append((current_period_close / prev_period_close) - 1.0)
        prev_key = k

    plt.title('%s returns distribution (%s)' % (symbol, interval))
    plt.xlabel('Returns (%)')
    plt.ylabel('Frequency (%)')
    plt.hist(returns, normed=True, bins=25)
    plt.show()

show_returns_distribution(sys.argv[1], sys.argv[2])
