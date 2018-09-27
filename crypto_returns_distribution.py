import sys
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

import alpha_vantage

def show_returns_distribution(base_currency, interval):
    data = alpha_vantage.get_crypto_price_history(base_currency, 'USD', interval)
    meta_key, dates_key = data
    dates_data = data[dates_key]

    returns = []
    prev_key = None

    for k, v in dates_data.items():
        if prev_key != None:
            prev_period_close = float(dates_data[prev_key]['4a. close (USD)'])
            current_period_close = float(v['4a. close (USD)'])
            returns.append((current_period_close / prev_period_close) - 1.0)
        prev_key = k

    print("Average return: %f" % np.mean(returns))

    plt.title('%s returns distribution (%s)' % (base_currency, interval))
    plt.xlabel('Returns (%)')
    plt.ylabel('Frequency (%)')
    plt.hist(returns, normed=True, bins=25)
    plt.show()

show_returns_distribution(sys.argv[1], sys.argv[2])
