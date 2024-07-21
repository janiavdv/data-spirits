import pandas as pd
import sqlite3


df = pd.read_csv("data/FRED.csv")

conn = sqlite3.connect('data/data.db')
c = conn.cursor()
c.execute('DROP TABLE IF EXISTS "sales";')

create_table = '''
CREATE TABLE sales (
    year INTEGER,
    month INTEGER,
    amount_sold INTEGER
);
'''
c.execute(create_table)


# Iterate through each row
for index, row in df.iterrows():
    # Extract year, month, and value from the 'DATE' and 'VALUE' columns
    year, month, _ = row['DATE'].split('-')
    sold = row['MRTSSM4453USN']
    insert_bet = '''INSERT INTO sales (year, month, amount_sold) VALUES (?, ?, ?)'''
    c.execute(insert_bet, (year, month, int(sold)))
    
conn.commit()





