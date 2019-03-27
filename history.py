import matplotlib
import sys
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import alpha_vantage


def show_history(symbol, interval='MONTHLY'):
    data = alpha_vantage.get_stock_price_history(
        symbol,
        interval,
        adjusted=False
    )

    plt.plot(list(data.keys()), list(data.values()))

    plt.title('%s price history' % symbol)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.show()


show_history(sys.argv[1])
