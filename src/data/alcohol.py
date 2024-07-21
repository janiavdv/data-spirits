import requests
import pandas as pd
import sqlite3

# SOURCE_URL = "http://localhost:8000/data/pcyr1970-2021.txt"
SOURCE_URL = "https://www.niaaa.nih.gov/sites/default/files/pcyr1970-2021.txt"
r = requests.get(SOURCE_URL)
data = r.text

num2state = {
 1:   "Alabama",
 2:   "Alaska",
 4:   "Arizona",
 5:   "Arkansas",
 6:   "California",
 8:   "Colorado",
 9:   "Connecticut",
10:   "Delaware",
11:   "DC",
12:   "Florida",
13:   "Georgia",
15:   "Hawaii",
16:   "Idaho",
17:   "Illinois",
18:   "Indiana",
19:   "Iowa",
20:   "Kansas",
21:   "Kentucky",
22:   "Louisiana",
23:   "Maine",
24:   "Maryland",
25:   "Massachusetts",
26:   "Michigan",
27:   "Minnesota",
28:   "Mississippi",
29:   "Missouri",
30:   "Montana",
31:   "Nebraska",
32:   "Nevada",
33:   "New Hampshire",
34:   "New Jersey",
35:   "New Mexico",
36:   "New York",
37:   "North Carolina",
38:   "North Dakota",
39:   "Ohio",
40:   "Oklahoma",
41:   "Oregon",
42:   "Pennsylvania",
44:   "Rhode Island",
45:   "South Carolina",
46:   "South Dakota",
47:   "Tennessee",
48:   "Texas",
49:   "Utah",
50:   "Vermont",
51:   "Virginia",
53:   "Washington",
54:   "West Virginia",
55:   "Wisconsin",
56:   "Wyoming"
}

num2bev_type = {
1:   "Spirits",
2:   "Wine",
3:   "Beer",
4:   "All beverages",
}

#  1-4    Year (4-digit calendar year)
#  6-7    Geographic ID code (FIPS code, see specification below)
#  9      Type of beverage (see specification below)
#  11-20  Gallons of beverage
#  22-30  Gallons of ethanol (absolute alcohol)
#  32-40  Population (age 14 and older)
#  43-47  Gallons of ethanol per capita age 14 and older
#           **(divide per capita gallons by 10,000 to obtain correct value)**
#  49-50  Decile for per capita consumption age 14 and older
#            (1 if state is ranked in top 10% by per capita consumption,
#             2 if in 10%-20%, etc.)
#  52-60  Population (age 21 and older)
#  63-67  Gallons of ethanol per capita age 21 and older
#           **(divide per capita gallons by 10,000 to obtain correct value)**
#  69-70  Decile for per capita consumption age 21 and older
#  72     Type of data source
#  74-76  Time-varying alcohol by volume (ABV)
#           **(divide ABV by 1,000 to obtain correct value)**
#  78-86  Gallons of ethanol derived from time-varying ABV
 
conn = sqlite3.connect('data/data.db')
c = conn.cursor()
c.execute('DROP TABLE IF EXISTS "alcohol";')

create_table = '''
CREATE TABLE alcohol (
    year INTEGER,
    state VARCHAR(50),
    beverage_type VARCHAR(50),
    gallons INTEGER
);
'''

c.execute(create_table)

for line in data.splitlines()[129:]:
    if len(line) < 21:
        continue
    year = line[0:4]
    geo_id = line[5:7].strip()
    beverage_id = line[8]
    gallons = line[11:20].strip()
    if gallons != '.' and int(geo_id) not in [91, 92, 93, 94, 99]:
        insert_bet = '''INSERT INTO alcohol (year, state, beverage_type, gallons) VALUES (?, ?, ?, ?)'''
        c.execute(insert_bet, (year, num2state[int(geo_id)], num2bev_type[int(beverage_id)], int(gallons)))
conn.commit()
 