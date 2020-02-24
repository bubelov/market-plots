import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
import matplotlib.style as style


def apply_common_styles():
    plt.figure(figsize=(38.4 / 2, 21.6 / 2))

    plt.rcParams['font.size'] = 20

    plt.rcParams['text.color'] = '#ffffff'

    plt.rcParams['axes.titlepad'] = 24
    plt.rcParams['axes.labelpad'] = 12
    plt.rcParams['axes.facecolor'] = '#222222'
    plt.rcParams['axes.labelcolor'] = '#ffffff'

    plt.rcParams['savefig.facecolor'] = '#111111'

    plt.rcParams['xtick.color'] = '#ffffff'
    plt.rcParams['xtick.major.pad'] = 12
    plt.rcParams['xtick.minor.pad'] = 12

    plt.rcParams['ytick.color'] = '#ffffff'
    plt.rcParams['ytick.major.pad'] = 12
    plt.rcParams['ytick.minor.pad'] = 12

    plt.rcParams['lines.linewidth'] = 3

    plt.rcParams['patch.force_edgecolor'] = True

    plt.rcParams['axes.spines.left'] = False
    plt.rcParams['axes.spines.right'] = False
    plt.rcParams['axes.spines.top'] = False
    plt.rcParams['axes.spines.bottom'] = False

    # gca means "get current axes"
    ax = plt.gca()
    ax.set_facecolor('#111111')
    ax.tick_params(axis=u'both', which=u'both', length=0)
    ax.yaxis.set_major_formatter(
        tkr.FuncFormatter(lambda x, p: format(int(x), ',')))
    #ax.grid(False)


def line():
    style.use('bmh')
    apply_common_styles()


def hist():
    style.use('default')
    apply_common_styles()


def scatter():
    style.use('bmh')
    apply_common_styles()
