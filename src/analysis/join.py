import sqlite3

conn = sqlite3.connect('data/data.db')

c = conn.cursor()
c.execute('DROP TABLE IF EXISTS "all_data";')

all_data_query = """
CREATE TABLE all_data AS
SELECT 
	bets.year,
	bets.month,
	bets.state,
	bets.gross_revenue,
	bets.hold,
	bets.handle,
	alcohol_sales.beer,
	alcohol_sales.spirits,
	alcohol_sales.wine,
	population_month.pop
FROM bets
JOIN alcohol_sales ON bets.year = alcohol_sales.year
                   AND bets.month = alcohol_sales.month
                   AND bets.state = alcohol_sales.state
JOIN population_month ON bets.year = population_month.year
                       AND bets.month = population_month.month
                       AND bets.state = population_month.state

"""
      
c.execute(all_data_query)

