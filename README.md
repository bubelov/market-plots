# Market Plots

A bunch of Python scripts that can be used to plot financial data

## Prerequisites

1. Python 3
2. [Alpha Vantage](https://www.alphavantage.co/) API key (it's free)

## Installing

```bash
git clone git@github.com:bubelov/market-plots.git
cd market-plots
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
echo ALPHA_VANTAGE_KEY=**YOUR_API_KEY** > .env
```

## Plotting History

```bash
python history.py SPX
```

## Plotting Variance

```bash
python variance.py TSLA
```

## Comparing Returns

```bash
python compare.py TSLA SPX
```

## Efficient Frontier (2 Assets)

```bash
python frontier2.py IBM DIS
```

## Efficient Frontier (N Assets)

```bash
python frontier.py IBM DIS KO
```
