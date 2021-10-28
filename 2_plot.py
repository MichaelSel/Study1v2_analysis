import seaborn as sns
from misc_funcs import *
import matplotlib.pyplot as plt

"""The data structure used for seaborn"""
format_general = [
    {
        'static': {
            'type': 'chromatic',
        },
        'dynamic': {
            'subject': 'subject',
            'shifted-swapped': 'chromatic_sh-sw',
            'length': 'melody_length',
            'rt_shifted': 'RT_chromatic_shifted',
            'rt_swapped': 'RT_chromatic_swapped'

        }
    },
    {
        'static': {
            'type': 'diatonic',
        },
        'dynamic': {
            'subject': 'subject',
            'shifted-swapped': 'diatonic_sh-sw',
            'length': 'melody_length',
            'rt_shifted': 'RT_diatonic_shifted',
            'rt_swapped': 'RT_diatonic_swapped'
        }
    }
]


def plot_bias():
    """plotting the bias ("% chose shifted- % chose swapped") in either condition (chromatic / diatonic) in every melody
    length (8/12/16) """

    # load and restructure the data to fit the seaborn format
    df = csv_to_pandas('./processed_data.csv', format_general)
    df['length'] = df['length'].astype('float')
    df['shifted-swapped'] = df['shifted-swapped'].astype('float')

    sns.catplot(data=df, kind="bar", x="length", y="shifted-swapped", hue="type")
    plt.show()


def plot_RT():
    """Plotting the delta in reaction times (RT_shifted - RT_swapped) in either condition (chromatic / diatonic) in
    every melody length (8 / 12 / 16) """

    format_RT = [
        {
            'static': {
                'type': 'shifted',
            },
            'dynamic': {
                'ch-dia': 'RT_shifted_c-d',
                'length': 'melody_length',
            }
        },
        {
            'static': {
                'type': 'swapped',
            },
            'dynamic': {
                'ch-dia': 'RT_swapped_c-d',
                'length': 'melody_length',
            }
        },
    ]
    # load and restructure the data to fit the seaborn format
    df = csv_to_pandas('./processed_data.csv', format_RT)
    df['length'] = df['length'].astype('float')
    df['ch-dia'] = df['ch-dia'].astype('float')
    sns.catplot(data=df, kind="bar", x="type", y="ch-dia", hue="length")
    plt.title("RT Delta")

    plt.show()


def plot_RT_hist():
    """plotting the distribution of RTs"""

    format_RT_dist = [
        {
            'static': {
                'type': 'rt',
            },
            'dynamic': {
                'rt': 'rt',
                'length': 'length',
            }
        },
    ]

    # load and restructure the data to fit the seaborn format
    df = csv_to_pandas('./trial_data.csv', format_RT_dist)
    df['length'] = df['length'].astype('float')
    df['rt'] = df['rt'].astype('float')

    sns.histplot(
        df,
        x="rt", hue="length",
        multiple="stack",
        palette="light:m_r",
        edgecolor=".3",
        linewidth=.5,
    )
    plt.xlim([0,5000])
    plt.show()


def plot_RTs_by_melody_length(length=8):
    format_RTs = [
        {
            'static': {
                'chose': 'shifted',
                'type': 'diatonic'
            },
            'dynamic': {
                'rt': 'RT_diatonic_shifted',
                'length': 'melody_length'
            }
        },
        {
            'static': {
                'chose': 'swapped',
                'type': 'diatonic'
            },
            'dynamic': {
                'rt': 'RT_diatonic_swapped',
                'length': 'melody_length'
            }
        },
        {
            'static': {
                'chose': 'shifted',
                'type': 'chromatic'
            },
            'dynamic': {
                'rt': 'RT_chromatic_shifted',
                'length': 'melody_length'
            }
        },
        {
            'static': {
                'chose': 'swapped',
                'type': 'chromatic'
            },
            'dynamic': {
                'rt': 'RT_chromatic_swapped',
                'length': 'melody_length'
            }
        },
    ]

    df = csv_to_pandas('./processed_data.csv', format_RTs)
    df['length'] = df['length'].astype('float')
    df['rt'] = df['rt'].astype('float')
    df = df[df['length'] == length]
    bar = sns.catplot(data=df, kind="bar", x="type", y="rt", hue="chose")
    plt.title(str(length) + " Note Melody")

    plt.show()


plot_bias()
# plot_RT()
# plot_RT_hist()
# plot_RTs_by_melody_length(8)
# plot_RTs_by_melody_length(12)
# plot_RTs_by_melody_length(16)