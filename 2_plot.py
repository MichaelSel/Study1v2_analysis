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
            'rt_delta': 'RT_chromatic_sh-sw'

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
            'rt_delta': 'RT_diatonic_sh-sw'
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

    # load and restructure the data to fit the seaborn format
    df = csv_to_pandas('./processed_data.csv', format_general)
    df['length'] = df['length'].astype('float')
    df['rt_delta'] = df['rt_delta'].astype('float')
    sns.catplot(data=df, kind="bar", x="length", y="rt_delta", hue="type")
    plt.show()


plot_bias()
plot_RT()
