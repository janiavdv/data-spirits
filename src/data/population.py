import sqlite3
import pandas as pd

def insert(years_list, df):
    for state in states_to_keep:
        for year_column in years_list:
            year = int(year_column[-4:])
            num = df.loc[df['NAME'] == state, year_column].values[0]
            insert_bet = '''INSERT INTO population (year, state, pop) VALUES (?, ?, ?)'''
            c.execute(insert_bet, (year, state, int(num)))

# Read the CSV files
census_pop_2000_2010 = pd.read_csv("data/st-est00int-alldata.csv")
census_pop_2010_2020 = pd.read_csv("data/nst-est2020-popchg2010-2020.csv")
census_pop_2020_2023 = pd.read_csv("data/NST-EST2023-POPCHG2020_2023.csv")


states_to_keep = [
    'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California',
    'Colorado', 'Connecticut', 'Delaware', 'District of Columbia', 'Florida',
    'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas',
    'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan',
    'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
    'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina',
    'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island',
    'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont',
    'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'
]


years_2000_2010 =  ['POPESTIMATE2000', 'POPESTIMATE2001', 'POPESTIMATE2002', 'POPESTIMATE2003', 'POPESTIMATE2004', 'POPESTIMATE2005', 'POPESTIMATE2006', 'POPESTIMATE2007', 'POPESTIMATE2008', 'POPESTIMATE2009', 'POPESTIMATE2010']
years_2011_2020 = ['POPESTIMATE2011', 'POPESTIMATE2012', 'POPESTIMATE2013', 'POPESTIMATE2014', 'POPESTIMATE2015', 'POPESTIMATE2016', 'POPESTIMATE2017', 'POPESTIMATE2018', 'POPESTIMATE2019', 'POPESTIMATE2020']
years_2021_2023 = ['POPESTIMATE2021', 'POPESTIMATE2022', 'POPESTIMATE2023']

conn = sqlite3.connect('data/data.db')
c = conn.cursor()
c.execute('DROP TABLE IF EXISTS "population";')

create_table = '''
CREATE TABLE population (
    year INTEGER,
    state VARCHAR(50),
    pop INTEGER
);
'''
c.execute(create_table)

insert(years_2000_2010, census_pop_2000_2010)
insert(years_2011_2020, census_pop_2010_2020)
insert(years_2021_2023, census_pop_2020_2023)

conn.commit()

