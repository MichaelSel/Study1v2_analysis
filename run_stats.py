from stat_funcs import *
import pandas as pd

# per-subject data
data = pd.read_csv("./processed_data.csv")

# only the 12-note cohort
only12 = data[data['melody_length']==12]

# the vector of diatonic shifted-swapped in the 12-note cohort
dia12_diffs = only12['diatonic_sh-sw'].reset_index()['diatonic_sh-sw']

# the vector of diatonic shifted-swapped in the 12-note cohort
chrom12_diffs = only12['chromatic_sh-sw'].reset_index()['chromatic_sh-sw']

# Cohen's Dz for diatonic 12 note melodies
cdz12 = cohen_dz(dia12_diffs-chrom12_diffs)

t12 = t_value(only12['diatonic_sh-sw'],only12['chromatic_sh-sw'])



# the vector of diatonic shifted-swapped in all cohorts
dia_diffs = data['diatonic_sh-sw'].reset_index()['diatonic_sh-sw']

# the vector of diatonic shifted-swapped in all cohorts
chrom_diffs = data['chromatic_sh-sw'].reset_index()['chromatic_sh-sw']

# Cohen's Dz for diatonic melodies
cdz = cohen_dz(dia_diffs-chrom_diffs)

t = t_value(data['diatonic_sh-sw'],data['chromatic_sh-sw'])



# only the 12 or 16 note cohort
only12_16 = data[data['melody_length']>8]

# the vector of diatonic shifted-swapped in the 12 or 16 note cohort
dia12_16_diffs = only12_16['diatonic_sh-sw'].reset_index()['diatonic_sh-sw']

# the vector of diatonic shifted-swapped in the 12 or 16 note cohort
chrom12_16_diffs = only12_16['chromatic_sh-sw'].reset_index()['chromatic_sh-sw']

# Cohen's Dz for diatonic 12 or 16 note melodies
cdz12_16 = cohen_dz(dia12_16_diffs-chrom12_16_diffs)

# T value for 12 or 16 note melodies
t12_16 = t_value(only12_16['diatonic_sh-sw'],only12_16['chromatic_sh-sw'])

print(1)