import sys
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import alpha_vantage

def show_variance(symbol, interval='MONTHLY'):
    returns = alpha_vantage.get_crypto_returns_history(symbol, interval)
    variance = np.var(returns)
    standard_deviation = np.sqrt(variance)

    plt.hist(returns, normed=True, bins=25)

    plt.xlabel('Returns (%)')
    plt.ylabel('Frequency')

    title_line_1 = '%s returns distribution (%s)' % (symbol, interval)
    title_line_2 = 'Variance = %f' % variance
    title_line_3 = 'Standard deviation = %f' % standard_deviation
    plt.title('%s\n%s\n%s' % (title_line_1, title_line_2, title_line_3))

    plt.show()

if len(sys.argv) > 2:
    show_variance(sys.argv[1], sys.argv[2])
else:
    show_variance(sys.argv[1])
