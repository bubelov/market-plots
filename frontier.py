import sys
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import alpha_vantage

def show_frontier(symbols, interval='MONTHLY'):
    print('Symbols: %s' % symbols)

    returns_history = dict()

    min_length = None

    for symbol in symbols:
        history = alpha_vantage.get_stock_returns_history(symbol, interval)
        print('Fetched %i records for symbol %s' % (len(history), symbol))

        if min_length == None:
            min_length = len(history)

        if (len(history) < min_length):
            min_length = len(history)

        returns_history[symbol] = history

    print('Min hisotry length = %i' % min_length)

    for symbol in symbols:
        returns_history[symbol] = returns_history[symbol][-min_length:]

    for symbol in symbols:
        print('History for symbol %s has %i records' % (symbol, len(returns_history[symbol])))

    mean_returns = dict()
    variances = dict()
    standard_deviations = dict()

    for symbol in symbols:
        history = returns_history[symbol]
        print('Return history for symbol %s has %i records' % (symbol, len(history)))
        mean_returns[symbol] = np.mean(history)
        variances[symbol] = np.var(history)
        standard_deviations[symbol] = np.sqrt(variances[symbol])

    portfolio_returns = []
    portfolio_deviations = []

    for i in range(0, 1_000):
        randoms = np.random.random_sample((len(symbols),))
        weights = [ random / sum(randoms) for random in randoms ]

        expected_return = sum([ weights[i] * mean_returns[symbol] for i, symbol in enumerate(symbols) ])

        weights_times_deviations = [ weights[i]**2 * standard_deviations[symbol]**2 for i, symbol in enumerate(symbols) ]
        variance = sum(weights_times_deviations)

        for i in range(0, len(symbols)):
            for j in range(0, len(symbols)):
                if (i != j):
                    symbol1 = symbols[i]
                    symbol2 = symbols[j]
                    #print('Pair = %s %s' % (symbol1, symbol2))

                    weight1 = weights[i]
                    weight2 = weights[j]
                    #print('Weights = %s %s' % (weight1, weight2))

                    deviation1 = standard_deviations[symbol1]
                    deviation2 = standard_deviations[symbol2]
                    #print('Deviations = %s %s' % (deviation1, deviation2))

                    correlation = np.corrcoef(returns_history[symbol1], returns_history[symbol2])[0][1]
                    #print('Correlation = %f' % correlation)

                    additional_variance = weight1 * weight2 * deviation1 * deviation2 * correlation
                    #print('Additional variance = %f' % additional_variance)

                    variance += additional_variance

        standard_deviation = np.sqrt(variance)
        #print('Portfolio expected return = %f' % expected_return)
        #print('Portfolio standard deviation = %f' % standard_deviation)

        plt.scatter(standard_deviation, expected_return, color='blue')

        portfolio_returns.append(expected_return)
        portfolio_deviations.append(standard_deviation)

    x_padding = np.average(portfolio_deviations) / 25
    plt.xlim(min(portfolio_deviations) - x_padding, max(portfolio_deviations) + x_padding)

    y_padding = np.average(portfolio_returns) / 25
    plt.ylim(min(portfolio_returns) - y_padding, max(portfolio_returns) + y_padding)

    plt.gca().set_xticklabels(['{:.2f}%'.format(x*100) for x in plt.gca().get_xticks()])
    plt.gca().set_yticklabels(['{:.2f}%'.format(y*100) for y in plt.gca().get_yticks()])

    plt.title('Efficient Frontier %s' % symbols)

    plt.xlabel('Risk')
    plt.ylabel('Return')

    plt.show()

show_frontier(sys.argv[1:])
