import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pathlib
import matplotlib.style as style

import alpha_vantage
import plot_style


def show_variance(symbol, interval='MONTHLY'):
    returns = alpha_vantage.get_stock_returns_history(symbol, interval)
    variance = np.var(returns)
    standard_deviation = np.sqrt(variance)
    mean_return = np.mean(returns)

    plot_style.hist()

    plt.gca().yaxis.set_major_formatter(
        matplotlib.ticker.StrMethodFormatter('{x:.0f}%'))

    plt.hist(returns, bins=25, edgecolor='white', linewidth=1)

    title_line_1 = f'{symbol} {interval} return distribution'
    title_line_2 = 'Standard deviation = %.2f%% Mean return = %.2f%%' % (
        standard_deviation * 100, mean_return * 100)

    plt.title(f'{title_line_1}\n{title_line_2}', pad=20)
    plt.xlabel('Return', labelpad=13)
    plt.ylabel('Frequency', labelpad=13)

    pathlib.Path('img/variance').mkdir(parents=True, exist_ok=True)
    plt.savefig(f'img/variance/{symbol}.png')
    plt.close()


show_variance(sys.argv[1])
