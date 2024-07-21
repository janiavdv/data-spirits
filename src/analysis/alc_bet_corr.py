import pandas as pd
from scipy.stats import spearmanr
import sqlite3
from termcolor import colored
import sys

sys.stdout = open('figures/correlations.txt', 'w') # Save the output to a file

conn = sqlite3.connect('data/data.db')
query = 'SELECT * FROM all_data'
all_data = pd.read_sql(query, conn)
all_data['total_alcohol'] = all_data['beer'] + all_data['spirits'] + all_data['wine'] # Calculate the total alcohol sales

def calculate_correlation(state_data: pd.DataFrame, bet: str, alcohol: str) -> pd.Series:
    """Calculate the Spearman correlation between two columns of a DataFrame.

    Args:
        state_data (pd.DataFrame): the data for a specific state
        bet (str): the column name of the first variable (bet)
        alcohol (str): the column name of the second variable (alcohol)

    Returns:
        pd.Series: a Series containing the correlation and p-value
    """
    
    correlation, p_value = spearmanr(state_data[bet], state_data[alcohol])
    return pd.Series({'correlation': correlation, 'p_value': p_value})


states = all_data.groupby('state')

handle_total = states.apply(calculate_correlation, bet='handle', alcohol='total_alcohol', include_groups=False)
handle_beer = states.apply(calculate_correlation, bet='handle', alcohol='beer', include_groups=False)
handle_spirits = states.apply(calculate_correlation, bet='handle', alcohol='spirits', include_groups=False)
handle_wine = states.apply(calculate_correlation, bet='handle', alcohol='wine', include_groups=False)

hold_total = states.apply(calculate_correlation, bet='hold', alcohol='total_alcohol', include_groups=False)
hold_beer = states.apply(calculate_correlation, bet='hold', alcohol='beer', include_groups=False)
hold_spirits = states.apply(calculate_correlation, bet='hold', alcohol='spirits', include_groups=False)
hold_wine = states.apply(calculate_correlation, bet='hold', alcohol='wine', include_groups=False)

gross_total = states.apply(calculate_correlation, bet='gross_revenue', alcohol='total_alcohol', include_groups=False)
gross_beer = states.apply(calculate_correlation, bet='gross_revenue', alcohol='beer', include_groups=False)
gross_spirits = states.apply(calculate_correlation, bet='gross_revenue', alcohol='spirits', include_groups=False)
gross_wine = states.apply(calculate_correlation, bet='gross_revenue', alcohol='wine', include_groups=False)


def display_significant_correlations(results: pd.DataFrame, description: str) -> None:
    """Display the states with strong and significant correlations.

    Args:
        results (pd.DataFrame): the results of the correlation analysis
        description (str): a description of the variables being compared
    """
    
    significant = results[results['p_value'] < 0.05]

    # Separate strong and weak correlations
    strong_correlation = significant[abs(significant['correlation']) > 0.5]
    weak_correlation = significant[abs(significant['correlation']) <= 0.5]

    print(f"Significant correlations for {description}:")

    # Print strong correlations in green
    if not strong_correlation.empty:
        print(colored("Strong Correlations (|correlation| > 0.5):", 'green'))
        print(colored(strong_correlation, 'green'))

    # Print weak correlations in red
    if not weak_correlation.empty:
        print(colored("Weak Correlations (|correlation| <= 0.5):", 'red'))
        print(colored(weak_correlation, 'red'))

    print("\n")


display_significant_correlations(handle_total, 'handle vs total alcohol')
display_significant_correlations(handle_beer, 'handle vs beer')
display_significant_correlations(handle_spirits, 'handle vs spirits')
display_significant_correlations(handle_wine, 'handle vs wine')

display_significant_correlations(hold_total, 'hold vs total alcohol')
display_significant_correlations(hold_beer, 'hold vs beer')
display_significant_correlations(hold_spirits, 'hold vs spirits')
display_significant_correlations(hold_wine, 'hold vs wine')

display_significant_correlations(gross_total, 'gross revenue vs total alcohol')
display_significant_correlations(gross_beer, 'gross revenue vs beer')
display_significant_correlations(gross_spirits, 'gross revenue vs spirits')
display_significant_correlations(gross_wine, 'gross revenue vs wine')


sys.stdout.close()

# Reset stdout so future prints will go to the console again
sys

# TODO: Do I need to do per capita since it's by state?