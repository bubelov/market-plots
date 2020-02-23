import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pathlib
import matplotlib.style as style

import alpha_vantage
from alpha_vantage import Interval
import plot_style


def show_variance(symbol, interval=Interval.MONTHLY):
    returns = alpha_vantage.get_stock_returns_history(symbol, interval)
    variance = np.var(returns)
    standard_deviation = np.sqrt(variance)
    mean_return = np.mean(returns)

    plot_style.hist()

    n, _, patches = plt.hist(returns, density=True, bins=25)

    for item in patches:
        item.set_height(item.get_height() / sum(n))

    max_y = max(n) / sum(n)
    plt.ylim(0, max_y + max_y / 10)

    plt.gca().set_xticklabels(['{:.0f}%'.format(x*100)
                               for x in plt.gca().get_xticks()])

    plt.gca().set_yticklabels(['{:.0f}%'.format(y*100)
                               for y in plt.gca().get_yticks()])

    title_line_1 = f'{symbol.upper()} {interval.value.lower().capitalize()} Return Distribution'
    title_line_2 = 'Standard Deviation = %.2f%% Mean Return = %.2f%%' % (
        standard_deviation * 100, mean_return * 100)
    plt.title(f'{title_line_1}\n{title_line_2}')
    plt.xlabel(f'{interval.value.lower().capitalize()} Return')
    plt.ylabel('Probability')

    pathlib.Path('img/variance').mkdir(parents=True, exist_ok=True)
    plt.savefig(f'img/variance/{symbol}.png')
    plt.close()


show_variance(sys.argv[1])
