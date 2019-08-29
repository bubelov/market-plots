# Market Plots

A bunch of Python scripts that can be used to plot financial data

# Prerequisites

1. Python 3
2. [Alpha Vantage](https://www.alphavantage.co/) API key (it's free)

# Installing

git clone git@github.com:bubelov/market-plots.git

cd market-plots

python3 -m venv venv

. venv/bin/activate

pip install -r requirements.txt

echo ALPHA_VANTAGE_KEY=**YOUR_API_KEY** > .env

# Plotting History

python history.py SPX

# Plotting Variance

python variance.py TSLA

# Comparing Returns

python compare.py TSLA SPX

# Efficient Frontier (2 Assets)

python frontier2.py IBM DIS

# Efficient Frontier (N Assets)

python frontier.py IBM DIS KO