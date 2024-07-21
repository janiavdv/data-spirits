import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import scipy.stats as stats

conn = sqlite3.connect('data/data.db')
query = "SELECT * FROM all_data"
all_data = pd.read_sql_query(query, conn)
states = all_data['state'].unique()

state_freq = {s: 0 for s in states}
for i, s1 in enumerate(states):
    for s2 in states[i+1:]:
        state_data1 = all_data[all_data['state'] == s1]
        state_data2 = all_data[all_data['state'] == s2]
        data1 = (state_data1['handle']/state_data1['pop']).values
        data2 = (state_data2['handle']/state_data2['pop']).values
        test_statistic, p_value = stats.ttest_ind(data1, data2)
        if p_value < 0.05:
            state_freq[s1] += 1
            state_freq[s2] += 1

print(state_freq)

fig, ax = plt.subplots(figsize=(9, 6), dpi=300)

ax.bar(state_freq.keys(), state_freq.values())
ax.set_xticklabels(state_freq.keys(), rotation=90)
fig.subplots_adjust(bottom=0.3)
ax.set_title('Frequency of States Occuring in Independent Pairs')
ax.set_ylabel('Frequency State is Independent from Another State')
fig.savefig('figures/bar_handle_per_capita.png')