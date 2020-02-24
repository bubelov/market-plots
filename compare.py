import sys
import pathlib
import matplotlib.pyplot as plt
from typing import List

import alpha_vantage
from alpha_vantage import Interval, AssetPrice
import plot_style


def compare(symbol_1: str,
            symbol_2: str,
            interval=Interval.MONTHLY,
            adjusted=True):
    history_1 = alpha_vantage.get_stock_price_history(
        symbol_1, interval, adjusted)

    history_2 = alpha_vantage.get_stock_price_history(
        symbol_2, interval, adjusted)

    history_1 = [v for v in history_1 if v.date in list(
        i.date for i in history_2)]

    history_2 = [v for v in history_2 if v.date in list(
        i.date for i in history_1)]

    adjust_values(history_1, start=100.0)
    adjust_values(history_2, start=100.0)

    plot_style.line()

    plt.plot(
        list(i.date for i in history_1),
        list(i.price for i in history_1),
        label=symbol_1.upper())

    plt.plot(
        list(i.date for i in history_2),
        list(i.price for i in history_2),
        label=symbol_2.upper())

    title = f'{symbol_1.upper()} vs {symbol_2.upper()}'
    title = title + ' (adjusted)' if adjusted == True else title
    plt.title(title)
    plt.legend()

    pathlib.Path('img/compare').mkdir(parents=True, exist_ok=True)
    plt.savefig(f'img/compare/{symbol_1.lower()}-{symbol_2.lower()}.png')
    plt.close()


def adjust_values(data: List[AssetPrice], start: float):
    scale_factor = None

    for v in data:
        if scale_factor == None:
            scale_factor = v.price / start

        v.price = v.price / scale_factor


compare(sys.argv[1], sys.argv[2])
