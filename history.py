import sys
import pathlib
import matplotlib.pyplot as plt

import alpha_vantage
from alpha_vantage import Interval
import plot_style


def show_history(symbol: str):
    data = alpha_vantage.get_stock_price_history(
        symbol,
        Interval.MONTHLY,
        adjusted=False
    )

    plot_style.line()
    plt.title(f'{symbol.upper()} Price History')
    plt.plot(
        list(i.date for i in data),
        list(i.price for i in data))

    pathlib.Path('img/history').mkdir(parents=True, exist_ok=True)
    plt.savefig(f'img/history/{symbol.lower()}.png')
    plt.close()


show_history(sys.argv[1])
