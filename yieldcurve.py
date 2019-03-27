import matplotlib.pyplot as plt
from collections import OrderedDict
from requests import get
from xml.etree import ElementTree
from dateutil import parser as date_parser
import matplotlib
from dataclasses import dataclass
from typing import List
import operator
import matplotlib.style as style


TREASURY_FEED_URL = 'http://data.treasury.gov/feed.svc/DailyTreasuryYieldCurveRateData'

CACHE_PATH = 'yieldcurvedata.xml'

NO_DATA = -100.0


@dataclass
class YieldData:
    date: str
    rate1m: float
    rate2m: float
    rate3m: float
    rate6m: float
    rate1y: float
    rate2y: float
    rate3y: float
    rate5y: float
    rate7y: float
    rate10y: float
    rate20y: float
    rate30y: float


def download_data():
    with open(CACHE_PATH, 'wb') as file:
        response = get(TREASURY_FEED_URL)
        file.write(response.content)


def get_property(properties, key, default=None):
    result = properties.find(
        '{http://schemas.microsoft.com/ado/2007/08/dataservices}' + key
    ).text

    if result is None:
        return default
    else:
        return result


def parse_data() -> List[YieldData]:
    data = list()

    tree = ElementTree.parse(CACHE_PATH)
    root = tree.getroot()

    for entry in root.iter('{http://www.w3.org/2005/Atom}entry'):
        content = entry.find('{http://www.w3.org/2005/Atom}content')
        properties = content[0]

        item = YieldData(
            date=date_parser.parse(get_property(properties, 'NEW_DATE')),
            rate1m=float(get_property(properties, 'BC_1MONTH', NO_DATA)),
            rate2m=float(get_property(properties, 'BC_2MONTH', NO_DATA)),
            rate3m=float(get_property(properties, 'BC_3MONTH', NO_DATA)),
            rate6m=float(get_property(properties, 'BC_6MONTH', NO_DATA)),
            rate1y=float(get_property(properties, 'BC_1YEAR', NO_DATA)),
            rate2y=float(get_property(properties, 'BC_2YEAR', NO_DATA)),
            rate3y=float(get_property(properties, 'BC_3YEAR', NO_DATA)),
            rate5y=float(get_property(properties, 'BC_5YEAR', NO_DATA)),
            rate7y=float(get_property(properties, 'BC_7YEAR', NO_DATA)),
            rate10y=float(get_property(properties, 'BC_10YEAR', NO_DATA)),
            rate20y=float(get_property(properties, 'BC_20YEAR', NO_DATA)),
            rate30y=float(get_property(properties, 'BC_30YEAR', NO_DATA))
        )

        data.append(item)

    return data


def generate_yield_history_plot(data):
    data = list(filter(lambda item:
                       item.rate3m != NO_DATA
                       and item.rate2y != NO_DATA
                       and item.rate10y != NO_DATA,
                       data))

    dates = list(map(lambda item: item.date, data))
    rates3m = list(map(lambda item: item.rate3m, data))
    rates2y = list(map(lambda item: item.rate2y, data))
    rates10y = list(map(lambda item: item.rate10y, data))

    style.use('bmh')

    plt.figure(figsize=(38.4 / 2, 21.6 / 2))

    matplotlib.rcParams.update({'font.size': 22})

    plt.rcParams['xtick.major.pad'] = 12
    plt.rcParams['xtick.minor.pad'] = 12

    plt.rcParams['ytick.major.pad'] = 8
    plt.rcParams['ytick.minor.pad'] = 8

    plt.plot(dates, rates3m, antialiased=True, linewidth=2)
    plt.plot(dates, rates2y, antialiased=True, linewidth=2)
    plt.plot(dates, rates10y, antialiased=True, linewidth=2)

    plt.title('Treasury Yield History', pad=24)

    plt.xlabel('Date', labelpad=16)
    plt.ylabel('Yield (%)', labelpad=16)

    plt.savefig('img/treasury-yield-history.png')
    plt.close()


def generate_yield_curve_plot(rates):
    style.use('bmh')

    plt.figure(figsize=(38.4 / 2, 21.6 / 2))

    matplotlib.rcParams.update({'font.size': 22})

    plt.rcParams['xtick.major.pad'] = 12
    plt.rcParams['xtick.minor.pad'] = 12

    plt.rcParams['ytick.major.pad'] = 8
    plt.rcParams['ytick.minor.pad'] = 8

    plt.plot(
        [0.25, 0.5, 1, 2, 3, 5, 7, 10, 20, 30],
        [rates.rate3m, rates.rate6m, rates.rate1y,
         rates.rate2y, rates.rate3y, rates.rate5y,
         rates.rate7y, rates.rate10y, rates.rate20y,
         rates.rate30y]
    )

    date_string = rates.date.strftime("%Y-%m-%d")
    plt.title(f'Yield Curve for {date_string}', pad=24)
    plt.xlabel('Duration (years)', labelpad=16)
    plt.ylabel('Rate (%)', labelpad=16)

    plt.savefig(f'img/yield-curve-{date_string}.png')
    plt.close()


download_data()

data = sorted(parse_data(), key=operator.attrgetter('date'))
generate_yield_history_plot(data)

for day in data[-1:]:
    generate_yield_curve_plot(day)
