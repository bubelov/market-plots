import sys
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import alpha_vantage

def show_variance(symbol, interval='MONTHLY'):
    returns = alpha_vantage.get_stock_returns_history(symbol, interval)
    variance = np.var(returns)
    standard_deviation = np.sqrt(variance)
    mean_return = np.mean(returns)

    plt.hist(returns, normed=True, bins=25)

    title_line_1 = '%s returns distribution' % interval
    title_line_2 = 'Standard deviation = %.2f%% Mean return = %.2f%%' % (standard_deviation * 100, mean_return * 100)
    plt.title('%s\n%s' % (title_line_1, title_line_2))
    plt.xlabel('Returns')
    plt.ylabel('Frequency')
    plt.show()

show_variance(sys.argv[1])
