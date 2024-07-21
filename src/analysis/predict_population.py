import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score

import numpy as np

conn = sqlite3.connect('data/data.db')
query = "SELECT * FROM population"
df = pd.read_sql_query(query, conn)

# Create a pivot table: states as rows, years as columns, and population as values
df_pivot = df.pivot(index='state', columns='year', values='pop')

years = df_pivot.columns.values.astype(int)

def predict_population(state_data, predict_all=False):
    """
    Predict a state's population 2024 using a linear regression model of years 2000-2023.
    - input state_data: a row of the pivot table with years as index and populations as values
    - input predict_all: a boolean to predict all years from 2000-2023
    - return: the predicted population for 2024 (rounded to the nearest integer)
    """

    # Prepare the data for fitting the model
    X = years.reshape(-1, 1)  # Years as features
    y = state_data.values  # Populations as targets
    
    # Using Random Forest Regressor
    model = RandomForestRegressor(n_estimators=100)
    # 5-fold cross-validation
    cv_scores = cross_val_score(model, X, y, cv=5, scoring='r2')
    print("Average Cross-Validation Score (R^2):", np.mean(cv_scores))

    model.fit(X, y)
    
    if predict_all:
        # Predict all years from 2000-2023
        return model.predict(X)
    
    # Predict the population for 2024
    return model.predict(np.array([[2024]]))[0].round().astype(int)

# Apply the prediction function to each state
predicted_2024 = df_pivot.apply(predict_population, axis=1)

predicted_data = [(2024, state, pop) for state, pop in predicted_2024.items()]
assert len(predicted_data) == 51

# Insert the data 
insert_statement = "INSERT INTO population (year, state, pop) VALUES (?, ?, ?)"
c = conn.cursor()
c.executemany(insert_statement, predicted_data)
conn.commit()

fig, axs = plt.subplots(11, 5, figsize=(20, 40))  # 11 rows, 5 columns for 51 states (DC)
axs = axs.flatten()

for idx, state in enumerate(df_pivot.index):
    actual_data = df_pivot.loc[state].values
    predicted_data = predict_population(df_pivot.loc[state], predict_all=True)
    
    ax = axs[idx]
    ax.plot(years, actual_data, label='Actual Data', marker='o')
    ax.plot(years, predicted_data, label='Predicted', linestyle='--')
    ax.set_title(state)
    ax.set_xlabel('Year')
    ax.set_ylabel('Population')
    ax.legend()

plt.tight_layout()
plt.savefig('figures/population_predictions.png')
plt.show()