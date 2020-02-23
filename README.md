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
echo ALPHA_VANTAGE_KEY=YOUR_API_KEY > .env
```

## Plotting History

```bash
python history.py spx
```

```bash
tree img/

img/
└── [4.0K]  history
    └── [102K]  spx.png

display -update 1 img/history/spx.png
```

![History](/example-images/history.png)

## Plotting Variance

```bash
python variance.py tsla
```

![Variance](/example-images/variance.png)

## Comparing Returns

```bash
python compare.py TSLA SPX
```

![Comparing Returns](/example-images/compare.png)

## Efficient Frontier (2 Assets)

```bash
python frontier2.py IBM DIS
```

![Efficient Frontier (IBM, DIS)](/example-images/frontier2.png)

## Efficient Frontier (N Assets)

```bash
python frontier.py IBM DIS KO
```
![Efficient Frontier (IBM, DIS, KO)](/example-images/frontier.png)
