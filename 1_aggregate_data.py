from misc_funcs import *
import pandas as pd

"""Preparing the data"""
# flatten all of the subjects data into one big file. Once the new file is created, get its path
json_data_path = reformat_data(data_dir='./task_sets', prefix="S1C", processed_dir="./processed")['full_path']

# make panda from the entire data set
all_trials = pd.DataFrame(get_json(json_data_path))
AT = all_trials

print()
""" basic examples of possible manipulations: """
# only get chromatic trials
chromatic = AT[AT['type'] == 'chromatic']

# only get 8-note diatonic trials
dia8 = AT[(AT['type'] == 'diatonic') & (AT['length'] == 8)]

# get average RT grouped by subject
avg_RT_by_subject = AT.groupby('subject', as_index=False)['rt'].mean()

"""Real stuff:"""



def count_trials(S, i):
    """This function is used in lambda iterative processes, and returns 0 when value is nan or undefined"""
    try:
        return S[i]
    except:
        return 0

# Total per_subject diatonic trials
temp = AT[AT["type"] == "diatonic"].groupby(['subject'])['probe'].count().reset_index()
temp = temp.rename(columns={'probe':'# diatonic'})
AT = AT.merge(temp,on="subject")

# Total per_subject chromatic trials
temp = AT[AT["type"] == "chromatic"].groupby(['subject'])['probe'].count().reset_index()
temp = temp.rename(columns={'probe':'# chromatic'})
AT = AT.merge(temp,on="subject")

# Total trials where subject chose "shifted" in DIATONIC trials
temp = AT[(AT["chose"] == "shifted") & (AT["type"] == "diatonic")].groupby(['subject'])['probe'].count().reset_index()
temp = temp.rename(columns={'probe':'# diatonic chose shifted'})
AT = AT.merge(temp,on="subject")

# Total trials where subject chose "swapped" in DIATONIC trials
temp = AT[(AT["chose"] == "swapped") & (AT["type"] == "diatonic")].groupby(['subject'])['probe'].count().reset_index()
temp = temp.rename(columns={'probe':'# diatonic chose swapped'})
AT = AT.merge(temp,on="subject")

# Total trials where subject chose "neither" in DIATONIC trials
temp = AT[(AT["chose"] == "neither") & (AT["type"] == "diatonic")].groupby(['subject'])['probe'].count().reset_index()
temp = temp.rename(columns={'probe':'# diatonic chose neither'})
AT = AT.merge(temp,on="subject")

# Total trials where subject chose "shifted" in CHROMATIC trials
temp = AT[(AT["chose"] == "shifted") & (AT["type"] == "chromatic")].groupby(['subject'])['probe'].count().reset_index()
temp = temp.rename(columns={'probe':'# chromatic chose shifted'})
AT = AT.merge(temp,on="subject")

# Total trials where subject chose "swapped" in CHROMATIC trials
temp = AT[(AT["chose"] == "swapped") & (AT["type"] == "chromatic")].groupby(['subject'])['probe'].count().reset_index()
temp = temp.rename(columns={'probe':'# chromatic chose swapped'})
AT = AT.merge(temp,on="subject")

# Total trials where subject chose "neither" in CHROMATIC trials
temp = AT[(AT["chose"] == "neither") & (AT["type"] == "chromatic")].groupby(['subject'])['probe'].count().reset_index()
temp = temp.rename(columns={'probe':'# chromatic chose neither'})
AT = AT.merge(temp,on="subject")

# Total no_neither diatonic trials
AT['# diatonic_NN_trials'] = AT['# diatonic'] - AT['# diatonic chose neither']

# Total no_neither chromatic trials
AT['# chromatic_NN_trials'] = AT['# chromatic'] - AT['# chromatic chose neither']

# % of diatonic trials where the subject chose shifted/swapped/neither
AT['diatonic_rate_shifted'] = AT['# diatonic chose shifted'] / AT['# diatonic']
AT['diatonic_rate_swapped'] = AT['# diatonic chose swapped'] / AT['# diatonic']
AT['diatonic_rate_neither'] = AT['# diatonic chose neither'] / AT['# diatonic']

# % of diatonic trials where the subject chose shifted/swapped/neither
AT['chromatic_rate_shifted'] = AT['# chromatic chose shifted'] / AT['# chromatic']
AT['chromatic_rate_swapped'] = AT['# chromatic chose swapped'] / AT['# chromatic']
AT['chromatic_rate_neither'] = AT['# chromatic chose neither'] / AT['# chromatic']

# % of diatonic trials where the subject chose shifted/swapped when ignoring neither trials
AT['diatonic_rate_shifted (NN)'] = AT['# diatonic chose shifted'] / AT['# diatonic_NN_trials']
AT['diatonic_rate_swapped (NN)'] = AT['# diatonic chose swapped'] / AT['# diatonic_NN_trials']

# % of chromatic trials where the subject chose shifted/swapped when ignoring neither trials
AT['chromatic_rate_shifted (NN)'] = AT['# chromatic chose shifted'] / AT['# chromatic_NN_trials']
AT['chromatic_rate_swapped (NN)'] = AT['# chromatic chose swapped'] / AT['# chromatic_NN_trials']

# expressing the subject bias in %shifted - %swapped in both diatonic and chromatic conditions
AT['diatonic_shifted-swapped'] = AT['diatonic_rate_shifted'] - AT['diatonic_rate_swapped']
AT['chromatic_shifted-swapped'] = AT['chromatic_rate_shifted'] - AT['chromatic_rate_swapped']

# expressing the subject bias in %shifted - %swapped in both diatonic and chromatic conditions (when ignoring neithers)
AT['diatonic_shifted-swapped (NN)'] = AT['diatonic_rate_shifted (NN)'] - AT['diatonic_rate_swapped (NN)']
AT['chromatic_shifted-swapped (NN)'] = AT['chromatic_rate_shifted (NN)'] - AT['chromatic_rate_swapped (NN)']

# Saving the "totals" dataframe to file.
AT.to_csv("./trial_data.csv")

"""The data in AT is on the trial level. Creating a new variable that will hold the computed values at the subject 
level """

# Column to hold subject names
totals = pd.DataFrame(AT['subject'])

# Holds subject mean RT
totals['RT'] = AT.groupby('subject')['rt'].transform('mean')

# Holds RT in chromatic trials
totals['RT_chromatic'] = AT[AT['type'] == "chromatic"].groupby('subject')['rt'].transform('mean')

# Holds RT in diatonic trials
totals['RT_diatonic'] = AT[AT['type'] == "diatonic"].groupby('subject')['rt'].transform('mean')

# Holds RT in diatonic trials when the subject chose "shifted"
totals['RT_diatonic_shifted'] = AT[(AT['type'] == "diatonic") & (AT['chose'] == "shifted")].groupby('subject')[
    'rt'].transform('mean')

# Holds RT in diatonic trials when the subject chose "swapped"
totals['RT_diatonic_swapped'] = AT[(AT['type'] == "diatonic") & (AT['chose'] == "swapped")].groupby('subject')[
    'rt'].transform('mean')

# Holds RT in diatonic trials when the subject chose "neither"
totals['RT_diatonic_neither'] = AT[(AT['type'] == "diatonic") & (AT['chose'] == "neither")].groupby('subject')[
    'rt'].transform('mean')

# Holds RT in chromatic trials when the subject chose "shifted"
totals['RT_chromatic_shifted'] = AT[(AT['type'] == "chromatic") & (AT['chose'] == "shifted")].groupby('subject')[
    'rt'].transform('mean')

# Holds RT in diatonic trials when the subject chose "swapped"
totals['RT_chromatic_swapped'] = AT[(AT['type'] == "chromatic") & (AT['chose'] == "swapped")].groupby('subject')[
    'rt'].transform('mean')

# Holds RT in diatonic trials when the subject chose "neither"
totals['RT_chromatic_neither'] = AT[(AT['type'] == "chromatic") & (AT['chose'] == "neither")].groupby('subject')[
    'rt'].transform('mean')


# Holds the number of diatonic trials
totals['diatonic_trials'] = AT[(AT['type'] == "diatonic")].groupby('subject')['probe'].transform('count')

# Holds the number of chromatic trials
totals['chromatic_trials'] = AT[(AT['type'] == "chromatic")].groupby('subject')['probe'].transform('count')

# Holds the number of diatonic trials where the subject chose shifted
totals['diatonic_chose_shifted'] = AT[(AT['type'] == "diatonic") & (AT['chose'] == "shifted")].groupby('subject')[
    'probe'].transform('count')

# Holds the number of diatonic trials where the subject chose swapped
totals['diatonic_chose_swapped'] = AT[(AT['type'] == "diatonic") & (AT['chose'] == "swapped")].groupby('subject')[
    'probe'].transform('count')

# Holds the number of diatonic trials where the subject chose neither
totals['diatonic_chose_neither'] = AT[(AT['type'] == "diatonic") & (AT['chose'] == "neither")].groupby('subject')[
    'probe'].transform('count')

# Holds the number of diatonic trials (ignoring neithers)
totals['diatonic_trials (NN)'] = totals['diatonic_trials'] - totals['diatonic_chose_neither']

# Holds the number of chromatic trials where the subject chose shifted
totals['chromatic_chose_shifted'] = AT[(AT['type'] == "chromatic") & (AT['chose'] == "shifted")].groupby('subject')[
    'probe'].transform('count')

# Holds the number of chromatic trials where the subject chose swapped
totals['chromatic_chose_swapped'] = AT[(AT['type'] == "chromatic") & (AT['chose'] == "swapped")].groupby('subject')[
    'probe'].transform('count')

# Holds the number of chromatic trials where the subject chose neither
totals['chromatic_chose_neither'] = AT[(AT['type'] == "chromatic") & (AT['chose'] == "neither")].groupby('subject')[
    'probe'].transform('count')

# Holds the number of chromatic trials (ignoring neithers)
totals['chromatic_trials (NN)'] = totals['chromatic_trials'] - totals['chromatic_chose_neither']

# Holds the melody lengths each subject heard
totals['melody_length'] = AT.groupby('subject')['length'].transform('mean')

# fill empty rows, and remove duplicates
temp = totals['subject']
totals = totals.groupby(['subject']).ffill().bfill()
totals['subject'] = temp
totals = totals.drop_duplicates()

# RT delta (shifted-swapped) in diatonic trials
totals['RT_diatonic_sh-sw'] = totals['RT_diatonic_shifted'] - totals['RT_diatonic_swapped']

# RT delta (shifted-swapped) in chromatic trials
totals['RT_chromatic_sh-sw'] = totals['RT_chromatic_shifted'] - totals['RT_chromatic_swapped']

totals['RT_swapped_c-d'] = totals['RT_chromatic_swapped']-totals['RT_diatonic_swapped']
totals['RT_shifted_c-d'] = totals['RT_chromatic_shifted']-totals['RT_diatonic_shifted']

# % of diatonic trials where subject chose shifted
totals['rate_diatonic_shifted'] = totals['diatonic_chose_shifted'] / totals['diatonic_trials']

# % of diatonic trials where subject chose shifted (ignoring neithers)
totals['rate_diatonic_shifted (NN)'] = totals['diatonic_chose_shifted'] / totals['diatonic_trials (NN)']

# % of diatonic trials where subject chose swapped
totals['rate_diatonic_swapped'] = totals['diatonic_chose_swapped'] / totals['diatonic_trials']

# % of diatonic trials where subject chose swapped (ignoring neithers)
totals['rate_diatonic_swapped (NN)'] = totals['diatonic_chose_swapped'] / totals['diatonic_trials (NN)']

# % of diatonic trials where subject chose neither
totals['rate_diatonic_neither'] = totals['diatonic_chose_neither'] / totals['diatonic_trials']

# % of chromatic trials where subject chose shifted
totals['rate_chromatic_shifted'] = totals['chromatic_chose_shifted'] / totals['chromatic_trials']

# % of chromatic trials where subject chose shifted (ignoring neithers)
totals['rate_chromatic_shifted (NN)'] = totals['chromatic_chose_shifted'] / totals['chromatic_trials (NN)']

# % of chromatic trials where subject chose swapped
totals['rate_chromatic_swapped'] = totals['chromatic_chose_swapped'] / totals['chromatic_trials']

# % of chromatic trials where subject chose swapped (ignoring neithers)
totals['rate_chromatic_swapped (NN)'] = totals['chromatic_chose_swapped'] / totals['chromatic_trials (NN)']

# % of chromatic trials where subject chose neither
totals['rate_chromatic_neither'] = totals['chromatic_chose_neither'] / totals['chromatic_trials']

# diatonic % chose shifted - % chose swapped
totals['diatonic_sh-sw'] = totals['rate_diatonic_shifted'] - totals['rate_diatonic_swapped']

# diatonic % chose shifted - % chose swapped (ignoring neithers)
totals['diatonic_sh-sw (NN)'] = totals['rate_diatonic_shifted (NN)'] - totals['rate_diatonic_swapped (NN)']

# chromatic % chose shifted - % chose swapped
totals['chromatic_sh-sw'] = totals['rate_chromatic_shifted'] - totals['rate_chromatic_swapped']

# chromatic % chose shifted - % chose swapped (ignoring neithers)
totals['chromatic_sh-sw (NN)'] = totals['rate_chromatic_shifted (NN)'] - totals['rate_chromatic_swapped (NN)']

# Saving the "totals" dataframe to file.
totals.to_csv("./processed_data.csv")
