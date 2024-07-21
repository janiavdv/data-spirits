import sqlite3
import pandas as pd
import plotly.express as px

conn = sqlite3.connect('data/data.db')
alcohol_sales = pd.read_sql_query("SELECT * FROM alcohol_sales", conn)
population = pd.read_sql_query("SELECT * FROM population", conn)
bets = pd.read_sql_query("SELECT * FROM bets", conn)

# Get average population per state
population = population.groupby('state').mean()
avg_pop = population[['pop']]

bets = bets.groupby('state').mean().astype(int)
bets = bets.rename(index={'DC': 'District of Columbia'}) # Change DC to District of Columbia
# Get per capita
bets = bets.join(avg_pop)
bets['handle_percapita'] = bets['handle'] / bets['pop']
bets = bets[['handle_percapita']]

alcohol_sales['alcohol'] = alcohol_sales['beer'] + alcohol_sales['spirits'] + alcohol_sales['wine']
alcohol_sales = alcohol_sales.groupby('state').mean()
alcohol_sales = alcohol_sales.rename(index={'DC': 'District of Columbia'}) # Change DC to District of Columbia
alcohol_sales = alcohol_sales.join(avg_pop)
alcohol_sales['alcohol_percapita'] = alcohol_sales['alcohol'] / alcohol_sales['pop']
alcohol_sales = alcohol_sales[['alcohol_percapita']]

df = alcohol_sales.join(bets)

# Full state abbreviations dictionary
state_abbreviations = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", 
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", 
    "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID", 
    "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS", 
    "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD", 
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", 
    "Mississippi": "MS", "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", 
    "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ", 
    "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", 
    "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR", 
    "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC", 
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", 
    "Vermont": "VT", "Virginia": "VA", "Washington": "WA", 
    "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY", 
    "District of Columbia": "DC"
}

# Map state names (index) to state codes
df["state_code"] = df.index.map(state_abbreviations)

# Plot for alcohol_percapita
fig1 = px.choropleth(df,
                     locations="state_code",
                     locationmode="USA-states",
                     color="alcohol_percapita",
                     hover_name=df.index,
                     color_continuous_scale="Oranges",
                     labels={"alcohol_percapita": "Alcohol Consumption (Gallons Per Month) Per Capita"},
                     scope="usa",
                     title="United States Alcohol Consumption (Gallons)")

# Show the plot
fig1.show()

# Plot for handle_percapita
fig2 = px.choropleth(df,
                     locations="state_code",
                     locationmode="USA-states",
                     color="handle_percapita",
                     hover_name=df.index,
                     color_continuous_scale="Blues",
                     labels={"handle_percapita": "Handle (Dollars Per Month) Per Capita"},
                     scope="usa",
                     title="United States Bet Handle ($)")

# Show the plot
fig2.show() 