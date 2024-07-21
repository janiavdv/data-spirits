import sqlite3
import pandas as pd
from scipy.stats import ttest_ind
from itertools import combinations
import matplotlib.pyplot as plt



conn = sqlite3.connect('data/data.db')
query = "SELECT * FROM alcohol_sales"
df_alcohol = pd.read_sql_query(query, conn)

conn = sqlite3.connect('data/data.db')
query = "SELECT * FROM population_month"
df_pop = pd.read_sql_query(query, conn)
df_pop['state'] = df_pop['state'].replace('District of Columbia', 'DC')

conn = sqlite3.connect('data/data.db')
query = "SELECT * FROM all_data"
df_all = pd.read_sql_query(query, conn)

state_count = {}
for state in df_alcohol['state'].unique():
    state_count[state] = 0
total = 0
for alcohol in ['beer', 'spirits', 'wine']:
    for state1, state2 in combinations(df_alcohol['state'].unique(), 2):
        group1 = df_alcohol[df_alcohol['state'] == state1][alcohol].values/df_pop[df_pop['state'] == state1]['pop'].values
        group2 = df_alcohol[df_alcohol['state'] == state2][alcohol].values/df_pop[df_pop['state'] == state2]['pop'].values
        # Perform t-test
        t_stat, p_value = ttest_ind(group1, group2, )
        # Output the results

        if p_value < 0.01:
            total += 1
            state_count[state1] += 1
            state_count[state2] += 1
            # print(f"T-test of {alcohol} between {state1} and {state2}:")
            # print("T-statistic:", t_stat)
            # print("P-value:", p_value)
            # print("Reject null hypothesis: There is a significant difference between the groups.")

states = list(state_count.keys())
counts = list(state_count.values())

# Creating the bar graph
plt.figure(figsize=(15, 9))
plt.bar(states, counts, color='skyblue')
plt.xlabel('States')
plt.ylabel('Count')
plt.title('Count of States')
plt.xticks(rotation=45)  # Rotating x-axis labels for better readability
plt.tight_layout()  # Adjust layout to prevent clipping of labels
plt.savefig('figures/state_alcohol_sig_count.png')

print(state_count)
