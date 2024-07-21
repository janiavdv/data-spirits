import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

conn = sqlite3.connect('data/data.db')
query = "SELECT * FROM sales"
sales = pd.read_sql_query(query, conn)

query = "SELECT * FROM alcohol"
alcohol = pd.read_sql_query(query, conn)
alcohol = alcohol[alcohol['year'] >= 2022]

sales['year_total'] = sales.groupby('year')['amount_sold'].transform('sum')
sales['month_year_proportion'] = sales['amount_sold'] / sales['year_total']

# Calculate mean of Jan 2024 based on average of all past januaries
sales_month_1 = sales[sales['month'] == 1]
mean_month_1_proportion = sales_month_1['month_year_proportion'].mean()
sales.iloc[-1, sales.columns.get_loc('month_year_proportion')] = mean_month_1_proportion

sales = sales[sales['year'] >= 2022]

################################### plotting
mask = (alcohol['beverage_type'] == 'Beer') & (alcohol['state'] == 'Wisconsin')
wisconson_beer = alcohol[mask]
#####################################

# Combine beer, spirits, wine into one row
alcohol = alcohol.pivot_table(index=['year', 'state'], columns='beverage_type', values='gallons', fill_value=0)

years = []
months = []
states = []
beer = []
spirits = []
wine = []
# Calculate monthly proportions
for index, row in alcohol.iterrows():
    year = index[0]
    for index2, row2 in sales.iterrows():
        if year == row2['year']:
            years.append(int(year))
            months.append(int(row2['month']))
            states.append(index[1])
            beer.append(int(row['Beer'] * row2['month_year_proportion']))
            spirits.append(int(row['Spirits'] * row2['month_year_proportion']))
            wine.append(int(row['Wine'] * row2['month_year_proportion']))

################################## plotting
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(8, 6))
axes[0].scatter(wisconson_beer['year'], wisconson_beer['gallons'], color='blue')
axes[0].set_title('Wisconsin Beer (gallons)')

axes[1].scatter(sales['year'] + sales['month']/12, sales['month_year_proportion'], color='red')
axes[1].set_title('Sales per month (proportion)')

data = {'years': years, 'months': months, 'state': states, 'beer': beer, 'spirits': spirits, 'wine': wine}
df = pd.DataFrame(data)

mask = df['state'] == 'Wisconsin'
axes[2].scatter(df[mask]['years'] + df[mask]['months']/12, df[mask]['beer'], color='purple')
axes[2].set_title('[Predicted] Wisconsin Beer (gallons)')

plt.subplots_adjust(hspace=0.5) # add more space
plt.savefig('figures/scatter_of_beer_prediction.png')
# plt.show()
#################################

c = conn.cursor()
c.execute('DROP TABLE IF EXISTS "alcohol_sales";')

create_table = '''
CREATE TABLE alcohol_sales (
    year INTEGER,
    month INTEGER,
    state VARCHAR(50),
    beer INTEGER,
    spirits INTEGER,
    wine INTEGERcx
);
'''
c.execute(create_table)

for i in range(len(years)):
    insert_alcohol_sales = '''INSERT INTO alcohol_sales (year, month, state, beer, spirits, wine) VALUES (?, ?, ?, ?, ?, ?)'''
    c.execute(insert_alcohol_sales, (years[i], months[i], states[i], beer[i], spirits[i], wine[i]))

conn.commit()