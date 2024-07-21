import sqlite3

import requests
from bs4 import BeautifulSoup

## SPORTS BETTING REVENUE SCRAPING

'''
GOAL:
Year | Month | State | Handle | Gross revenue | Hold %
'''

REVENUE_URL = 'https://www.covers.com/betting/betting-revenue-tracker'

r = requests.get(REVENUE_URL)
soup = BeautifulSoup(r.text, 'html.parser')

months = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "June": 6, "Jun": 6, "July": 7, "Jul": 7, "Aug": 8, "Sept": 9, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}

def clean_data(row):
    row_array = list(filter(lambda y: y != "", row.text.replace("$", "").replace(",", "").replace("%", "").split("\n")))
    
    if row_array[0] in months:
        row_array[0] = months[row_array[0]]
    
        if row_array[1] != "N/A":
            row_array[1] = float(row_array[1])
        else: 
            row_array[1] = None
        
        if row_array[2] != "N/A":
            row_array[2] = float(row_array[2])
        else:
            row_array[2] = None
        
        if row_array[3] != "N/A":
            row_array[3] = round(1/100 * float(row_array[3]), 3)
        else:
            row_array[3] = None
    
        return row_array  


tables = {} # name of table --> table data
headers = soup.find_all("h2") # the headers of each state and some extra headers
# [1:] to skip summary, [:32] only states, not misc titles
for i, inner_header in enumerate(headers[1:32]):
    while (inner_header := inner_header.find_next("h3")):
        if "monthly" in inner_header.text.lower():
            tables[inner_header.text.replace("\xa0", "")] = list(map(clean_data, inner_header.find_next("table").find_all("tr")))

conn = sqlite3.connect('data/data.db')
c = conn.cursor()
c.execute('DROP TABLE IF EXISTS "bets";')

create_table = '''
CREATE TABLE bets (
    year INTEGER,
    month INTEGER,
    state VARCHAR(50),
    handle REAL,
    gross_revenue REAL,
    hold REAL
);
'''

c.execute(create_table)

for key in tables.keys():
    index = key.find("20")
    year = int(key[index:index + 4])
    state = key[:index].strip()

    for value in tables[key]:
        if not value:
            # if month table --> skip
            continue

        # month: 1 is January, 2 is February, etc.
        month, handle, gross_revenue, hold = value

        if not (handle or gross_revenue or hold):
            # if a value is None, skip
            continue

        # Year | Month | State | Handle | Gross revenue | Hold %
        insert_bet = '''INSERT INTO bets (year, month, state, handle, gross_revenue, hold) VALUES (?, ?, ?, ?, ?, ?)'''
        c.execute(insert_bet, (year, month, state, handle, gross_revenue, hold))

conn.commit()