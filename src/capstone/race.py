import sqlite3
import pandas as pd
# #[
#   {date: "2000-01-01", name: "Coca-Cola", category: "Beverages", value: 72537},
#   {date: "2000-01-01", name: "Microsoft", category: "Technology", value: 35000},
#   {date: "2000-01-01", name: "IBM", category: "Technology", value: 34200},
#   {date: "2000-01-01", name: "General Electric", category: "Conglomerate", value: 33700},
#   {date: "2000-01-01", name: "Intel", category: "Technology", value: 33700},
#   {date: "2000-01-01", name: "Nokia", category: "Technology", value: 33000},

#   {date: "2001-01-01", name: "Microsoft", category: "Technology", value: 60000},
#   {date: "2001-01-01", name: "Coca-Cola", category: "Beverages", value: 60000},
#   {date: "2001-01-01", name: "IBM", category: "Technology", value: 52600},
#   {date: "2001-01-01", name: "General Electric", category: "Conglomerate", value: 52400},
#   {date: "2001-01-01", name: "Intel", category: "Technology", value: 50900},
#   {date: "2001-01-01", name: "Nokia", category: "Technology", value: 50000},
# …

def string_data(category):
    conn = sqlite3.connect('data/data.db')
    df = pd.read_sql_query("SELECT * FROM all_data", conn)
    # have the df only contain the year, month, state, and population columns
    df = df[['year', 'month', 'state', category, 'pop']]
    
    # combine the year, month column into one colum w/ values lile year-month-01
    df['date'] = df['year'].astype(str) + '-' + df['month'].astype(str) + '-01'
    # drop the year and month columns
    df = df.drop(columns=['year', 'month'])

    # order the df by date
    df = df.sort_values(by='date')
    data = []
    for _, row in df.iterrows():
        date = row['date']
        state = row['state']
        val = (row[category]/row['pop'])*10_000 # per 10,000 people
        string = f'{{"date": "{date}", "name": "{state}", "value": {val}}}'
        data.append(string)
    return data


def category_json():
    categories = ['wine', 'beer', 'spirits', 'handle']
    for c in categories:
        data = string_data(c)
        # store data in json format
        with open('data/' + c + '.json', 'w') as f:
            f.write('[')
            for i in range(len(data)):
                f.write(data[i])
                if i != len(data) - 1:
                    f.write(', ')
            f.write(']')


''' Look at yearly data for each beverage type using alcohol table'''
def string_data_by_year(bev_type):
    conn = sqlite3.connect('data/data.db')
    df = pd.read_sql_query("SELECT * FROM alcohol", conn)
    # change the year column to date and append a 01-01 to the end of the year
    df['date'] = df['year'].astype(str) + '-01-01'
    
    # order the df by date
    df = df.sort_values(by='date')
    # drop rows where beverage_type != bev_type
    df = df[df['beverage_type'] == bev_type]
    data = []
    for _, row in df.iterrows():
        date = row['date']
        state = row['state']
        val = row['gallons']
        string = f'{{"date": "{date}", "name": "{state}", "value": {val}}}'
        data.append(string)
    return data
   

''' Look at yearly data for each beverage type 1970-2020'''
def category_json_yearly():
    categories = ['Wine', 'Beer', 'Spirits']
    for c in categories:
        data = string_data_by_year(c)
        # store data in json format
        with open('data/race_json/' + c + '_yearly.json', 'w') as f:
            f.write('[')
            for i in range(len(data)):
                f.write(data[i])
                if i != len(data) - 1:
                    f.write(', ')
            f.write(']')

# category_json()
category_json_yearly()