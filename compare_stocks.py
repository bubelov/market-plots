import sys
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

import alpha_vantage

def compare(stock_symbol, benchmark_symbol, interval='MONTHLY'):
    stock_dates, stock_prices = alpha_vantage.get_stock_price_history(stock_symbol, interval, adjusted=True)
    benchmark_dates, benchmark_prices = alpha_vantage.get_crypto_price_history(benchmark_symbol, interval)

    stock_data = dict(zip(stock_dates, stock_prices))
    benchmark_data = dict(zip(benchmark_dates, benchmark_prices))

    stock_data = { k:v for (k,v) in stock_data.items() if k in benchmark_data.keys() }
    benchmark_data = { k:v for (k,v) in benchmark_data.items() if k in stock_data.keys() }

    stock_data = adjust_values(stock_data)
    benchmark_data = adjust_values(benchmark_data)

    covariance = np.cov(list(stock_data.values()), list(benchmark_data.values()), ddof=0)[0][1]
    benchmark_variance = np.var(list(benchmark_data.values()))
    beta = covariance / benchmark_variance

    correlation = np.corrcoef(list(stock_data.values()), list(benchmark_data.values()))
    print('Correllation: %s' % correlation)

    plt.plot(stock_data.keys(), stock_data.values(), label=stock_symbol)
    plt.plot(benchmark_data.keys(), benchmark_data.values(), label=benchmark_symbol)

    plt.xlabel('Date')
    plt.ylabel('Price (USD)')

    title_line_1 = '%s performance against %s (adjusted)' % (stock_symbol, benchmark_symbol)
    title_line_2 = 'Covariance = %f' % covariance
    title_line_3 = 'Benchmark variance = %f' % benchmark_variance
    title_line_4 = 'Beta = %f' % beta

    plt.title('%s\n%s\n%s\n%s' % (title_line_1, title_line_2, title_line_3, title_line_4))
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
