import matplotlib.pyplot as plt
import matplotlib.style as style


def apply_common_styles():
    plt.figure(figsize=(38.4 / 2, 21.6 / 2))

    plt.rcParams['font.size'] = 20

    plt.rcParams['axes.facecolor'] = '#ffffff'
    plt.rcParams['savefig.facecolor'] = '#ffffff'

    plt.rcParams['xtick.major.pad'] = 13
    plt.rcParams['xtick.minor.pad'] = 13

    plt.rcParams['ytick.major.pad'] = 13
    plt.rcParams['ytick.minor.pad'] = 13

    ax = plt.gca()
    ax.set_facecolor('#222222')


def line():
    style.use('bmh')
    apply_common_styles()


def hist():
    style.use('default')
    apply_common_styles()
