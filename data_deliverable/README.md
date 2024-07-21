Our project is studying the interaction between alcohol consumption and sports betting.

# Data Spec

Our data was gathered from a variety of sources. Scraped from niaaa.nih.gov, and www.covers.com, and dataset sets from fred.stlouisfed.org and the census (`src/` files have the scraping and cleaning code). We added all our data to the `data/data.db` database (after cleaning the data).

The database contains sports bets volume, and alcohol volume (and type) for each state for each year. Here is the schema:

* `alcohol (year INTEGER, state VARCHAR(50), beverage_type VARCHAR(50), gallons INTEGER)`
* `sales (year INTEGER, month INTEGER, amount_sold INTEGER);`
* `bets (year INTEGER, month INTEGER, state VARCHAR(50), handle REAL, gross_revenue REAL, hold REAL)`
* `population (year INTEGER, state VARCHAR(50), pop INTEGER);`

In the `alcohol` table, each entry is the alcohol volume per year for each state. The `beverage_type` is one of "Spirits", "Wine", "Beer", or "All beverages". The `gallons` is the number of gallons bought per year. Each `state` (including DC) and `year` pair is unique. We ensure no NULLs.

In the `sales` table, each entry is the alcohol volume per month for the entire US. We need this table because the `alcohol` table doesn't have month-by-month granularity.  We will combine the two tables under simple assumptions to get by-state monthly alcohol statistics.

In the `bets` table, the `handle` (>0) is the total amount wagered, the `hold` (between 0 and 100) is a percentage of the handle that the sports book kept from the handle. The `gross_revenue` (>0) was the total revenue of the sports books. We expect the tuples `(year, month, and state)` to not have repeats. We ensure no NULLs.

In the `population` table, `pop` is the population that `year` in that `state`. Nothing is NULLs and the pairs `(year, state)` are unique.

# Attributes

## handle
This attribute is present in the `bets` tables. There is no default value for this attribute. The range of this value is 259180.26 - 2122331713.0. The values are skewed, most likely due to the differing populations in states. These values are not unique. They will not be used to identify duplicate records. The `handle` attribute is a required value. These values will be used to determine if the hold amount is dependent on alcohol consumption. The value does not contain any sensitive information.

## month
This attribute is present in the `sales` and `bets` tables. There is no default value for this attribute. We encode the month as an integer. The value has 12 options: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12. We have roughly equal amounts of data for each month. The values are not unique (many data points share the same month). This value will be a key for time series questions/research directions. We didn't have duplicate records in our data sets, so we won't need to do any deduplication. This attribute is a required value for all of our data points, but none of the rows were missing it. There is no sensitive information contained in this value.

## pop
This attribute is present in the `population` table. There is no default value. The range is 494300 - 39437610. The distribution of these values is skewed since the population is dependent on various external factors. These values are not unique. They will not be used to identify duplicate records. This attribute is a required value. We plan on using these values to calculate per capita values in other tables. This attribute does not contain sensitive information.

## amount_sold
This attribute is present in the `sales` table. There is no default value for this attribute. The range of values is 1501 - 8021. The values are roughly equally distributed, but the overall average increased each year, and December typically had the highest sales within each year. These values are not unique. This attribute will not be used to detect duplicate records. This is a required value, as it is the most important part of the table. This attribute is going to be used to calculate the monthly consumption of alcohol by state. This attribute does not contain sensitive information.

## beverage_type
This attribute is present in the `alcohol` table. There is no default value for this attribute. The value has 3 options: Wine, Spirit, and Beer. In a simplified analysis, in the `alcohol` tables, a majority of the `gallons` belong to beer, followed by wine, followed by spirits. These values are not unique. These values will be used in tandem with `state` and `year` in the table to remove duplicate values. This is a required value; the data point is not useful if this value is missing. These values will be used in the final analysis to see if sports betting is affected by the consumption of different alcohol types. This attribute does not contain any sensitive information.

## gallons
This is an attribute present in the `alcohol` table. There is no default value for this attribute. The range of values is: 236000 - 795212000. The values are not uniformly distributed due to other external factors (the state's population mainly). These values are mostly unique. This value will not be used to detect duplicate records. This is a required value since it is what we are mainly interested in, in this table. This attribute is going to be used to help estimate the gallons consumed by state by beverage type for the years 2022-2024. This attribute does not contain any sensitive information.

## state

One attribute present in all our tables is `state` attribute. There is no default value for this attribute, if data does not contain a value for this attribute it will be removed. It includes all 50 states and DC, except in the `bets` table which only contains states where sports betting is legal. There is roughly equal data for each state in each table. The values in this attribute are not completely unique, as tables will contains several values from the same state. This column is typically used (in tandem with other columns) to help detect duplicate values in tables. This attribute is going to be a big focus of our analysis since all of our analysis will be done on a by state by month level.

## year
Another attribute present in most of our tables in the `year` attribute. There is no default value for this attribute. The `population` table contains a range of year values from 2000-2023, the `alcohol` table contains a year values from 1970-2021, and the `sales` table contains year values from 1992-2024. The distribution is equal for these values, as each year contains the same amount of data. These values are used in tandem with other attributes to help detect duplicate values. This is a required value, the datapoint will be removed if it does not contain a year value. This attribute is going to be used in the analysis to estimate population in 2024, as well as alcohol consumption by state from 2022-2024. This attribute will not be used in the final analysis though. This feature does not contain any sensitive information.

# Link to dataset

Find the `data.db` file [here](https://github.com/csci1951a-spring-2024/final-project-data-spirits/blob/main/data/data.db).

# Sample data

We've provided a sample of 100 rows (across each table). The first row of each sample data is the column names.

```
year|state|pop
2000|Alabama|4452173
2001|Alabama|4467634
2002|Alabama|4480089
2003|Alabama|4503491
2004|Alabama|4530729
2005|Alabama|4569805
2006|Alabama|4628981
2007|Alabama|4672840
2008|Alabama|4718206
2009|Alabama|4757938
2010|Alabama|4785298
2000|Alaska|627963
2001|Alaska|633714
2002|Alaska|642337
2003|Alaska|648414
2004|Alaska|659286
2005|Alaska|666946
2006|Alaska|675302
2007|Alaska|680300
2008|Alaska|687455
=====================
year|state|beverage_type|gallons
1970|Alabama|Spirits|3863000
1970|Alabama|Wine|1412000
1970|Alabama|Beer|33098000
1970|Alaska|Spirits|945000
1970|Alaska|Wine|470000
1970|Alaska|Beer|5372000
1970|Arizona|Spirits|2967000
1970|Arizona|Wine|2508000
1970|Arizona|Beer|38604000
1970|Arkansas|Spirits|1865000
1970|Arkansas|Wine|1193000
1970|Arkansas|Beer|22378000
1970|California|Spirits|45071000
1970|California|Wine|58590000
1970|California|Beer|363645000
1970|Colorado|Spirits|4494000
1970|Colorado|Wine|3132000
1970|Colorado|Beer|42145000
1970|Connecticut|Spirits|7277000
1970|Connecticut|Wine|4726000
=====================
year|month|state|handle|gross_revenue|hold
2023|1|Arizona|591220793.69|47486816.94|0.08
2023|2|Arizona|609278096.0|35392452.0|0.058
2023|3|Arizona|644763990.55|53523946.62|0.083
2023|4|Arizona|535712027.03|49163322.65|0.092
2023|5|Arizona|451717025.0|49595605.0|0.109
2023|6|Arizona|393198857.89|28331607.97|0.072
2023|7|Arizona|323211485.27|35343494.78|0.109
2023|8|Arizona|358875474.29|31681151.15|0.088
2023|9|Arizona|610716285.1|60115066.43|0.098
2023|10|Arizona|648208573.06|56868980.77|0.088
2023|11|Arizona|713586703.92|42333281.89|0.059
2023|12|Arizona|693310960.0|67697686.0|0.098
2022|1|Arizona|563694591.18|41890200.2|0.074
2022|2|Arizona|491665553.76|25629834.77|0.052
2022|3|Arizona|690979294.05|38898393.33|0.056
2022|4|Arizona|512877847.67|30441991.88|0.059
2022|5|Arizona|461450688.26|56193285.87|0.122
2022|6|Arizona|318774198.34|12601356.09|0.04
2022|7|Arizona|290511532.54|22684581.19|0.078
2022|8|Arizona|361008835.14|37161758.62|0.103
=====================
year|month|amount_sold
1992|1|1509
1992|2|1541
1992|3|1597
1992|4|1675
1992|5|1822
1992|6|1775
1992|7|1912
1992|8|1862
1992|9|1770
1992|10|1882
1992|11|1831
1992|12|2511
1993|1|1614
1993|2|1529
1993|3|1678
1993|4|1713
1993|5|1796
1993|6|1792
1993|7|1950
1993|8|1777
```

# Tech Report

Located here: `data_deliverable/reports/tech_reports/README.md`.
