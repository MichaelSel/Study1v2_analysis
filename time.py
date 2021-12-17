import json
import dateutil.parser
import matplotlib.pyplot as plt
import statistics as stat
import pandas as pd
import seaborn as sns


#define directories
processed_dir = './processed'
analyzed_dir = './analyzed'
all_data_path = processed_dir + "/S1C_all_subjects.json"



def get_json(path):
        json_file = open(path)
        json_file = json_file.read()
        return json.loads(json_file)



all_subjects = get_json(all_data_path)
AS = pd.DataFrame(all_subjects)
AS = AS[AS['length']==12] #only 12-note melodies
AS['time'] = pd.to_datetime(AS['time'])
AS['Q_num'] = AS['Q_num'].astype('float')
AS['time_elapsed'] = AS['time_elapsed'].astype('float')

AS.sort_values(['subject','Q_num'], ascending=[True,True], inplace=True)
AS['shift'] = AS.groupby('subject')['time_elapsed'].shift()
AS['diff_from_previous_trial (s)'] = AS['time_elapsed'] - AS['shift']
AS['diff_from_previous_trial (s)'] = AS['diff_from_previous_trial (s)']/1000
subjects = AS['subject'].unique()
subjects.sort()
max = AS.groupby(['subject'], sort=True)['time'].max()
min = AS.groupby(['subject'], sort=True)['time'].min()
diff = max-min

num_of_trials = AS.groupby(['subject'], sort=True)['probe'].count()
frame = { 'Subject': subjects, 'Task Duration': diff, '# Trials': num_of_trials}
totals = pd.DataFrame(frame)
totals['Task Duration (min)'] = (totals['Task Duration']).dt.total_seconds()/60
totals['Mean Trial Duration (secs)'] = (totals['Task Duration (min)']*60)/totals['# Trials']



# plt.hist(totals['Task Duration (min)'].tolist(), density=True, bins=200)  # `density=False` would make counts
# plt.xlim([0, 100])
# plt.show()


print("test")
data = AS.dropna()
data = data[data['diff_from_previous_trial (s)']>0]
data = data[data['diff_from_previous_trial (s)']<30]


print("test")

sns.histplot(data=data, x="diff_from_previous_trial (s)", bins=20)
plt.show()


print('\n\n')
# print("Average time for entire study",stat.mean(times),'minutes.')
# print("Median time for entire study",stat.median(times),'minutes.')
# print("Fastest time for entire study",min(times),'minutes.')
# print("Slowest time for entire study",max(times),'minutes.')
# print('\n')
#
# print("Average time per question",stat.mean(times)*60/100,'seconds.')
# print("Median time per question",stat.median(times)*60/100,'seconds.')
# print("Fastest time per question",min(times)*60/100,'seconds.')
# print("Slowest time per question",max(times)*60/100,'seconds.')