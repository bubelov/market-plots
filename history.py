import sys
import pathlib
import matplotlib.pyplot as plt

import alpha_vantage
import plot_style


def show_history(symbol: str, interval='MONTHLY'):
    data = alpha_vantage.get_stock_price_history(
        symbol,
        interval,
        adjusted=False
    )

    plot_style.line()
    plt.title(f'{symbol.upper()} Price History')
    plt.plot(list(data.keys()), list(data.values()))

    pathlib.Path('img/history').mkdir(parents=True, exist_ok=True)
    plt.savefig(f'img/history/{symbol.lower()}.png')
    plt.close()


show_history(sys.argv[1])
