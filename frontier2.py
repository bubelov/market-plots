import sys
import pathlib
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import alpha_vantage
from alpha_vantage import Interval
import plot_style


def show_frontier(symbol1: str,
                  symbol2: str,
                  interval=Interval.MONTHLY):
    returns1 = alpha_vantage.get_stock_returns_history(symbol1, interval)
    returns2 = alpha_vantage.get_stock_returns_history(symbol2, interval)

    if len(returns1) > len(returns2):
        returns1 = returns1[-len(returns2):]

    if len(returns2) > len(returns1):
        returns2 = returns2[-len(returns1):]

    mean_returns1 = np.mean(returns1)
    variance1 = np.var(returns1)
    standard_deviation1 = np.sqrt(variance1)

    #print(f'Mean returns ({symbol1}) = {mean_returns1}')
    #print(f'Variance ({symbol1}) = {variance1}')
    #print(f'Standard Deviation ({symbol1}) = {standard_deviation1}')

    mean_returns2 = np.mean(returns2)
    variance2 = np.var(returns2)
    standard_deviation2 = np.sqrt(variance2)

    #print(f'Mean returns ({symbol2}) = {mean_returns2}')
    #print(f'Variance ({symbol2}) = {variance2}')
    #print(f'Standard Deviation ({symbol2}) = {standard_deviation2}')

    correlation = np.corrcoef(returns1, returns2)[0][1]
    #print(f'Corellation = {correlation}')

    weights = []

    for n in range(0, 101):
        weights.append((1 - 0.01 * n, 0 + 0.01 * n))

    returns = []
    standard_deviations = []

    portfolio_50_50_standard_deviation = None
    portfolio_50_50_returns = None

    plot_style.scatter()

    for w1, w2 in weights:
        returns.append(w1 * mean_returns1 + w2 * mean_returns2)

        variance = w1**2 * standard_deviation1**2 + w2**2 * standard_deviation2**2 + \
            2 * w1 * w2 * standard_deviation1 * standard_deviation2 * correlation

        standard_deviation = np.sqrt(variance)
        standard_deviations.append(standard_deviation)

        plt.scatter(standard_deviations[-1], returns[-1], color='#007bff')

        if w1 == 0.5 and w2 == 0.5:
            portfolio_50_50_standard_deviation = standard_deviations[-1]
            portfolio_50_50_returns = returns[-1]

    plt.scatter(portfolio_50_50_standard_deviation,
                portfolio_50_50_returns, marker='x', color='red', alpha=1, s=320)

    x_padding = np.average(standard_deviations) / 25

    plt.xlim(min(standard_deviations) - x_padding,
             max(standard_deviations) + x_padding)

    y_padding = np.average(returns) / 25

    plt.ylim(min(returns) - y_padding, max(returns) + y_padding)

    plt.gca().set_xticklabels(['{:.2f}%'.format(x*100)
                               for x in plt.gca().get_xticks()])
    plt.gca().set_yticklabels(['{:.2f}%'.format(y*100)
                               for y in plt.gca().get_yticks()])

    plt.title(f'Efficient Frontier ({symbol1.upper()} and {symbol2.upper()})')

    plt.xlabel(f'Risk ({interval.value.lower().capitalize()})')
    plt.ylabel(f'Return ({interval.value.lower().capitalize()})')

    pathlib.Path('img/frontier2').mkdir(parents=True, exist_ok=True)
    plt.savefig(f'img/frontier2/{symbol1.lower()}-{symbol2.lower()}.png')
    plt.close()


show_frontier(sys.argv[1], sys.argv[2])
