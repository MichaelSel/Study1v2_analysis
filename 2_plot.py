import seaborn as sns
from misc_funcs import *
import matplotlib.pyplot as plt
import pandas as pd

"""The data structure used for seaborn"""
format_general = [
    {
        'static': {
            'type': 'chromatic',
        },
        'dynamic': {
            'subject': 'subject',
            'length': 'melody_length',
            'rt': 'RT_chromatic',
            'rt_shifted': 'RT_chromatic_shifted',
            'rt_swapped': 'RT_chromatic_swapped',
            'rt_neither': 'RT_chromatic_neither',
            'rt_sh-sw': 'RT_chromatic_sh-sw',
            'rt_sh-sw': 'RT_chromatic_sh-sw',
            'rate_shifted': 'rate_chromatic_shifted',
            'rate_shifted (NN)': 'rate_chromatic_shifted (NN)',
            'rate_swapped': 'rate_chromatic_swapped',
            'rate_swapped (NN)': 'rate_chromatic_swapped (NN)',
            'rate_neither': 'rate_chromatic_neither',
            'sh-sw': 'chromatic_sh-sw',
            'sh-sw (NN)': 'chromatic_sh-sw (NN)',
        }
    },
    {
        'static': {
            'type': 'diatonic',
        },
        'dynamic': {
            'subject': 'subject',
            'length': 'melody_length',
            'rt': 'RT_diatonic',
            'rt_shifted': 'RT_diatonic_shifted',
            'rt_swapped': 'RT_diatonic_swapped',
            'rt_neither': 'RT_diatonic_neither',
            'rt_sh-sw': 'RT_diatonic_sh-sw',
            'rt_sh-sw': 'RT_diatonic_sh-sw',
            'rate_shifted': 'rate_diatonic_shifted',
            'rate_shifted (NN)': 'rate_diatonic_shifted (NN)',
            'rate_swapped': 'rate_diatonic_swapped',
            'rate_swapped (NN)': 'rate_diatonic_swapped (NN)',
            'rate_neither': 'rate_diatonic_neither',
            'sh-sw': 'diatonic_sh-sw',
            'sh-sw (NN)': 'diatonic_sh-sw (NN)',
        }
    }
]
format_general2 = [
    {
        'static': {
            'type': 'chromatic',
            'condition': 'shifted'
        },
        'dynamic': {
            'subject': 'subject',
            'length': 'melody_length',
            'rate': 'rate_chromatic_shifted',
        }
    },
    {
        'static': {
            'type': 'chromatic',
            'condition': 'swapped'
        },
        'dynamic': {
            'subject': 'subject',
            'length': 'melody_length',
            'rate': 'rate_chromatic_swapped',
        }
    },
    {
        'static': {
            'type': 'chromatic',
            'condition': 'neither'
        },
        'dynamic': {
            'subject': 'subject',
            'length': 'melody_length',
            'rate': 'rate_chromatic_neither',
        }
    },
    {
        'static': {
            'type': 'diatonic',
            'condition': 'shifted'
        },
        'dynamic': {
            'subject': 'subject',
            'length': 'melody_length',
            'rate': 'rate_diatonic_shifted',
        }
    },
    {
        'static': {
            'type': 'diatonic',
            'condition': 'swapped'
        },
        'dynamic': {
            'subject': 'subject',
            'length': 'melody_length',
            'rate': 'rate_diatonic_swapped',
        }
    },
    {
        'static': {
            'type': 'diatonic',
            'condition': 'neither'
        },
        'dynamic': {
            'subject': 'subject',
            'length': 'melody_length',
            'rate': 'rate_diatonic_neither',
        }
    },

]


def plot_bias():
    """plotting the bias ("% chose shifted- % chose swapped") in either condition (chromatic / diatonic) in every melody
    length (8/12/16) """

    # load and restructure the data to fit the seaborn format
    df = csv_to_pandas('./processed_data.csv', format_general)
    df['length'] = df['length'].astype('float')
    df['sh-sw'] = df['sh-sw'].astype('float')
    sns.catplot(data=df, kind="bar", x="length", y="sh-sw", hue="type")
    plt.show()


def plot_rate(length=16):
    """plotting the bias ("% chose shifted- % chose swapped") in either condition (chromatic / diatonic) in every melody
    length (8/12/16) """

    # load and restructure the data to fit the seaborn format
    df = csv_to_pandas('./processed_data.csv', format_general2)
    df['length'] = df['length'].astype('float')
    df['rate'] = df['rate'].astype('float')
    temp = df[df['length']==length]
    sns.catplot(data=temp, kind="bar", x="type", y="rate", hue="condition")
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
    plt.xlim([0, 5000])
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


plot_rate()
# plot_RT()
# plot_RT_hist()
# plot_RTs_by_melody_length(8)
# plot_RTs_by_melody_length(12)
# plot_RTs_by_melody_length(16)

# pro = pd.read_csv("processed_data.csv")
# frame1 = { 'rate_shifted': pro['pc_diatonic_shifted'], 'condition': 'diatonic' }
# frame1 = pd.DataFrame(frame1)
# frame2 = { 'rate_shifted': pro['pc_chromatic_shifted'], 'condition': 'chromatic' }
# frame2 = pd.DataFrame(frame2)
#
#
# pro = pd.concat([frame1,frame2]).reset_index()
#
# sns.displot(data=pro,x="rate_shifted")
# plt.show()
