import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3

conn = sqlite3.connect('data/data.db')
data = pd.read_sql_query("SELECT * FROM all_data", conn)

df = data
df['alcohol_percapita'] = (df['beer'] + df['spirits'] + df['wine'])/df['pop']
df['handle_percapita'] = df['handle']/df['pop']
df = df[['year', 'month', 'state', 'alcohol_percapita', 'handle_percapita']]

chosen_states = df[df['state'].isin(['Nevada', 'Rhode Island', 'New Hampshire'])].copy()
no_state = df.drop('state', axis=1)
national_avg = no_state.groupby('month').mean().reset_index()
# add 'National Average' to the state column
national_avg['state'] = 'National Average'


grouped = chosen_states.groupby(['state', 'month']).mean().reset_index()

# Set seaborn style
sns.set_style("darkgrid")

# Create a seaborn line plot
plt.figure(figsize=(5, 6))
sns.lineplot(data=grouped,      x='handle_percapita', y='alcohol_percapita', hue='state', marker='o', markersize=8, linewidth=1, sort=False)
# Plot the national average line
sns.lineplot(data=national_avg, x='handle_percapita', y='alcohol_percapita', hue='state', palette={'National Average': 'black'}, marker='o', markersize=8, linewidth=2, sort=False)

no = {('Rhode Island', 'Jan'), ('National Average', 'Feb')}
states_data = list(grouped.groupby('state'))
states_data.append(('National Average', national_avg))
for name, group in states_data:
    data = list(zip(group['handle_percapita'], group['alcohol_percapita']))
    for i, month in [(0, 'Jan'), (1, 'Feb'), (6, 'Jul'), (11, 'Dec')]:
        if (name, month) in no:
            continue
        x, y = data[i]
        dx, dy = {'Jan': (10., 0.), 'Feb': (-10, 0), 'Jul': (-1, 0.05), 'Dec': (-7, 0)}[month]
        plt.text(x+dx, y+dy, month, fontsize=10, ha='center', va='bottom')
        # plt.annotate(month, xy=(x,y), xytext=(x+dx, y+dy),
        #      arrowprops=dict(facecolor='black', edgecolor='black', arrowstyle=''), fontsize=10, ha='center', va='bottom')

# Set labels and title
plt.xlabel('Average Monthly Handle Per Capita')
plt.ylabel('Average Monthly Alcohol Per Capita')
plt.title('Alcohol vs Handle Per Capita by State')

# Add legend
plt.legend(title='State', bbox_to_anchor=(.5, 1), loc='upper left')

# Save figure
plt.tight_layout()
plt.savefig('analysis_deliverable/visualizations/3state_handle_alc.png', dpi=300)

# Show plot
plt.show()
