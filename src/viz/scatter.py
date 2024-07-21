import sqlite3
import pandas as pd
import plotly.express as px
from scipy.stats import spearmanr

conn = sqlite3.connect('data/data.db')
all_data = pd.read_sql_query("SELECT * FROM all_data", conn)

# Get the average handle per state using all_data
all_data = all_data.groupby('state').mean().astype(int)


states = list(all_data.index)
# convert states to there abbreviations
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
states = [state_abbreviations[state] for state in states]
handles = list(all_data['handle'])
alcohol = list(all_data['beer'] + all_data['spirits'] + all_data['wine'])
pops =  list(all_data['pop'])

# divide handles and alcohol by population
handles = [handle/pop for handle, pop in zip(handles, pops)]
alcohol = [alc/pop for alc, pop in zip(alcohol, pops)]

correlation, p_value = spearmanr(handles, alcohol)
print(f"The Spearman correlation between handles and alcohol sales is {correlation:.2f} with a p-value of {p_value:.2f}")

# scatter plot of handles vs alcohol size of the cicrle is the population label the points w/ the states using arrows
fig = px.scatter(x=handles, y=alcohol, size=pops, text = states, color=states, labels={'x': 'Average Monthly Handle Per Capita ($)', 'y': 'Average Monthly Alcohol Consumption Per Capita (Gallons)'}, title='Handle vs Alcohol Sales')
# set text position to be middle center
fig.update_traces(textposition='top center')
fig.update_layout(title='Average Monthly Handle Per Capita vs Average Monthly Alcohol Consumption Per Capita')
fig.show()
