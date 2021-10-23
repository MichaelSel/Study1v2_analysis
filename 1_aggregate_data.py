from misc_funcs import *
import pandas as pd

"""Preparing the data"""
# flatten all of the subjects data into one big file. Once the new file is created, get its path
json_data_path = reformat_data(data_dir='./task_sets', prefix="S1C", processed_dir="./processed")['full_path']

# make panda from the entire data set
all_trials = pd.DataFrame(get_json(json_data_path))

""" basic examples of possible manipulations: """
# only get chromatic trials
chromatic = all_trials[all_trials['type'] == 'chromatic']

# only get 8-note diatonic trials
dia8 = all_trials[(all_trials['type'] == 'diatonic') & (all_trials['length'] == 8)]

# get average RT grouped by subject
avg_RT_by_subject = all_trials.groupby('subject', as_index=False)['rt'].mean()

"""Real stuff:"""

# remove all the trials where the subject chose "neither" (keep in a variable called N(o)N(eithers))
NN = all_trials[all_trials['chose'] != 'neither']

# Add column with the total number of trials each subject saw.
NN['total_trials'] = NN.groupby(['subject'])['probe'].transform('count')


def count_trials(S, i):
    """This function is used in lambda iterative processes, and returns 0 when value is nan or undefined"""
    try:
        return S[i]
    except:
        return 0


# Total per_subject diatonic trials
temp = NN[NN["type"] == "diatonic"].groupby(['subject'])['probe'].count()
NN['diatonic_trials'] = NN.apply(lambda row: count_trials(temp, row.subject), axis=1)

# Total per_subject chromatic trials
temp = NN[NN["type"] == "chromatic"].groupby(['subject'])['probe'].count()
NN['chromatic_trials'] = NN.apply(lambda row: count_trials(temp, row.subject), axis=1)

# Total trials where subject chose "shifted" in DIATONIC trials
temp = NN[(NN["chose"] == "shifted") & (NN["type"] == "diatonic")].groupby(['subject'])['probe'].count()
NN['diatonic_chose_shifted'] = NN.apply(lambda row: count_trials(temp, row.subject), axis=1)

# Total trials where subject chose "swapped" in DIATONIC trials
temp = NN[(NN["chose"] == "swapped") & (NN["type"] == "diatonic")].groupby(['subject'])['probe'].count()
NN['diatonic_chose_swapped'] = NN.apply(lambda row: count_trials(temp, row.subject), axis=1)

# Total trials where subject chose "shifted" in CHROMATIC trials
temp = NN[(NN["chose"] == "shifted") & (NN["type"] == "chromatic")].groupby(['subject'])['probe'].count()
NN['chromatic_chose_shifted'] = NN.apply(lambda row: count_trials(temp, row.subject), axis=1)

# Total trials where subject chose "swapped" in CHROMATIC trials
temp = NN[(NN["chose"] == "swapped") & (NN["type"] == "chromatic")].groupby(['subject'])['probe'].count()
NN['chromatic_chose_swapped'] = NN.apply(lambda row: count_trials(temp, row.subject), axis=1)

# % of diatonic trials where the subject chose shifted/swapped
NN['PC_diatonic_chose_shifted'] = NN['diatonic_chose_shifted'] / NN['diatonic_trials']
NN['PC_diatonic_chose_swapped'] = NN['diatonic_chose_swapped'] / NN['diatonic_trials']

# % of chromatic trials where the subject chose shifted/swapped
NN['PC_chromatic_chose_shifted'] = NN['chromatic_chose_shifted'] / NN['chromatic_trials']
NN['PC_chromatic_chose_swapped'] = NN['chromatic_chose_swapped'] / NN['chromatic_trials']

# expressing the subject bias in %shifted - %swapped in both diatonic and chromatic conditions
NN['diatonic_shifted-swapped'] = NN['PC_diatonic_chose_shifted'] - NN['PC_diatonic_chose_swapped']
NN['chromatic_shifted-swapped'] = NN['PC_chromatic_chose_shifted'] - NN['PC_chromatic_chose_swapped']

"""The data in NN is on the trial level. Creating a new variable that will hold the computed values at the subject 
level """

# Column to hold subject names
totals = pd.DataFrame(NN['subject'])

# Holds subject mean RT
totals['RT'] = NN.groupby('subject')['rt'].transform('mean')

# Holds RT in chromatic trials
totals['RT_chromatic'] = NN[NN['type'] == "chromatic"].groupby('subject')['rt'].transform('mean')

# Holds RT in diatonic trials
totals['RT_diatonic'] = NN[NN['type'] == "diatonic"].groupby('subject')['rt'].transform('mean')

# Holds RT in diatonic trials when the subject chose "shifted"
totals['RT_diatonic_shifted'] = NN[(NN['type'] == "diatonic") & (NN['chose'] == "shifted")].groupby('subject')[
    'rt'].transform('mean')

# Holds RT in diatonic trials when the subject chose "swapped"
totals['RT_diatonic_swapped'] = NN[(NN['type'] == "diatonic") & (NN['chose'] == "swapped")].groupby('subject')[
    'rt'].transform('mean')

# Holds RT in chromatic trials when the subject chose "shifted"
totals['RT_chromatic_shifted'] = NN[(NN['type'] == "chromatic") & (NN['chose'] == "shifted")].groupby('subject')[
    'rt'].transform('mean')

# Holds RT in chromatic trials when the subject chose "swapped"
totals['RT_chromatic_swapped'] = NN[(NN['type'] == "chromatic") & (NN['chose'] == "swapped")].groupby('subject')[
    'rt'].transform('mean')

# Holds the number of (non-neither) diatonic trials
totals['diatonic_trials'] = NN[(NN['type'] == "diatonic")].groupby('subject')['probe'].transform('count')

# Holds the number of (non-neither) chromatic trials
totals['chromatic_trials'] = NN[(NN['type'] == "chromatic")].groupby('subject')['probe'].transform('count')

# Holds the number of diatonic trials where the subject chose shifted
totals['diatonic_chose_shifted'] = NN[(NN['type'] == "diatonic") & (NN['chose'] == "shifted")].groupby('subject')[
    'probe'].transform('count')

# Holds the number of diatonic trials where the subject chose swapped
totals['diatonic_chose_swapped'] = NN[(NN['type'] == "diatonic") & (NN['chose'] == "swapped")].groupby('subject')[
    'probe'].transform('count')

# Holds the number of chromatic trials where the subject chose shifted
totals['chromatic_chose_shifted'] = NN[(NN['type'] == "chromatic") & (NN['chose'] == "shifted")].groupby('subject')[
    'probe'].transform('count')

# Holds the number of chromatic trials where the subject chose swapped
totals['chromatic_chose_swapped'] = NN[(NN['type'] == "chromatic") & (NN['chose'] == "swapped")].groupby('subject')[
    'probe'].transform('count')

# Holds the melody lengths each subject heard
totals['melody_length'] = NN.groupby('subject')['length'].transform('mean')

# fill empty rows, and remove duplicates
temp = totals['subject']
totals = totals.groupby(['subject']).ffill().bfill()
totals['subject'] = temp
totals = totals.drop_duplicates()

# RT delta (shifted-swapped) in diatonic trials
totals['RT_diatonic_sh-sw'] = totals['RT_diatonic_shifted'] - totals['RT_diatonic_swapped']

# RT delta (shifted-swapped) in chromatic trials
totals['RT_chromatic_sh-sw'] = totals['RT_chromatic_shifted'] - totals['RT_chromatic_swapped']

# % of diatonic trials where subject chose shifted
totals['pc_diatonic_shifted'] = totals['diatonic_chose_shifted'] / totals['diatonic_trials']

# % of diatonic trials where subject chose swapped
totals['pc_diatonic_swapped'] = totals['diatonic_chose_swapped'] / totals['diatonic_trials']

# % of chromatic trials where subject chose shifted
totals['pc_chromatic_shifted'] = totals['chromatic_chose_shifted'] / totals['chromatic_trials']

# % of chromatic trials where subject chose swapped
totals['pc_chromatic_swapped'] = totals['chromatic_chose_swapped'] / totals['chromatic_trials']

# diatonic % chose shifted - % chose swapped
totals['diatonic_sh-sw'] = totals['pc_diatonic_shifted'] - totals['pc_diatonic_swapped']

# chromatic % chose shifted - % chose swapped
totals['chromatic_sh-sw'] = totals['pc_chromatic_shifted'] - totals['pc_chromatic_swapped']

# Saving the "totals" dataframe to file.
totals.to_csv("./processed_data.csv")
