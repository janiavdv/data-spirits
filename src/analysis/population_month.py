import pandas as pd
import sqlite3

conn = sqlite3.connect('data/data.db')

population_query = "SELECT * FROM population"
population = pd.read_sql_query(population_query, conn)

population = population[population['year'] >= 2022] # Filter for years 2022 and later

population_month = pd.DataFrame(columns=['year', 'month', 'state', 'population'])

for state, state_data in population.groupby('state'):
    # Iterate over each year
    for i, year in enumerate(range(2022, 2025)):
        # Calculate the total population for the current state and year
        total_population_year = state_data[state_data['year'] == year]['pop'].sum()
        
        # Calculate the total population for the next year if available
        if year < 2024:
            next_year_population = state_data[state_data['year'] == year + 1]['pop'].sum()
        else:
            prev_difference = total_population_year - state_data[state_data['year'] == year - 1]['pop'].sum()
            next_year_population = total_population_year + prev_difference
        
        # Calculate the linear increment per month between years
        increment_per_month = (next_year_population - total_population_year) / 12
        
        # Iterate over each month of the current year and assign the incremented population
        for month in range(1, 13):
            if year >= 2024 and month > 1:
                break
            
            row = pd.DataFrame({'year': year, 'month': month, 'state': state, 
                                'population': total_population_year + increment_per_month * (month - 1)},  index=[0])
            population_month = pd.concat([population_month, row], ignore_index=True)

population_month['population'] = population_month['population'].astype(int) 

# Insert the data into the database

c = conn.cursor()

c.execute('DROP TABLE IF EXISTS "population_month";')

create_table = '''
CREATE TABLE population_month (
    year INTEGER,
    month INTEGER,
    state VARCHAR(50),
    pop INTEGER
);
'''
c.execute(create_table)

insert_statement = "INSERT INTO population_month (year, month, state, pop) VALUES (?, ?, ?, ?)"
c.executemany(insert_statement, population_month.values.tolist())

conn.commit()