# Alcohol by year by state

## Question 1: 
This dataset contains 7956 data points, 156 per state (& DC) and 3 per state per year (for each alcohol type). It will be used to help estimate alcohol consumption by state for 2022-2024. With 51 years of data, this should be more than enough to make accurate predictions.

## Question 2:
The identifying columns in this table are `state`, `year`, and `beverage_type`.

## Question 3:
We collected the data from the National Institute of Alcohol Abuse and Alcoholism. Specifically, the aforementioned organization maintains a text file on its website containing the alcohol statistics mentioned above. This organization is a government body with an extensive research-based past, so this data is very likely accurate, and we consider the source reputable. The alcohol data was generated using a mix of sales and shipment data provided by beverage industry sources and volume/tax revenue data provided by the state. Given the length the NIAAA went to achieve accurate data and the diversity of sources it was collected from, the data seems unlikely to contain sampling errors.

## Question 4:
The data was completely clean and did not contain any missing values. In addition, the data contains no duplicate values either. Since the file was a text file, the `gallons` field did have to be converted to an integer. The data shows an apparent increase in the amount consumed for each state, though further analysis needs to be done to determine whether this is due to population increase only or also due to individuals consuming more alcohol. When examining the type of alcohol consumed, beer makes up about 85% of the total volume, spirits about 6% of the total volume, and wine about 9% of the total volume. While the data is skewed, it is essential to remember that these statistics are by volume rather than alcohol content. In terms of average gallons consumed, the top 5 states were California, Texas, New York, Florida, and Pennsylvania. The bottom 5 states were South Dakota, North Dakota, Vermont, Alaska, and Wyoming. Again, this is most likely explained by population, and further analysis should be done analyzing per capita alcohol consumption.


# Alcohol retail sales by month

## Question 1:
This dataset contains 385 data points. It includes the total retail sales amount for beer, wine, and liquor stores across the United States from January 1992 to January 2024. This dataset will be used to help estimate the alcohol sales by month by state in tandem with the above table. Since this data will only be used to calculate proportions, there should be no issue with lacking data.

## Question 2:
The identifying columns in this table are `year` and `month`.

## Question 3:
The St. Louis Federal Reserve collected the data. Given that this is a well-known government entity, the data is likely to be accurate and the source reputable. In addition, the broadness of the collection makes it likely that there is no sampling bias in the data.

## Question 4:
The data was provided as a downloadable csv from the FRED website. The data was completely clean, did not contain any missing values, and contained no duplicate values. Based on some EDA, it's clear that alcohol sales have steadily increased over time. In addition, sales experienced a significant spike in December and a minor low in February. Between March and November, alcohol sales seem to stay at a relatively consistent level.

# Sports bets by state by month

## Question 1:
This dataset contains 690 data points. The data is not distributed evenly. We only have 3 data points from Maine, 4 from Kentucky, 13 from Massachusetts, 13 from Ohio, 17 from Kansas, and 18 from Tennessee, and everything else has 24 or 25 data points. We expect this because sports betting has only recently been legalized in some states.

## Question 2:
The identifying attributes are `year`, `month`, and `state`.

## Question 3:
We got the data from www.covers.com. We scrapped the html tables from their website using Beautiful Soup. The code for that is in `src/bets.py`. They have been in sports betting since 1995 and have 20 million customers (according to Betting Planet). NYT, MSMBC, and ESPN often cite them. Thus, they seem to be reputable in the sports betting industry. The sample is all sports betting data aggregated by month and state. It is small because online sports betting was only legalized recently in many states and is new in general. It is unlikely to exhibit any sampling bias since it's an aggregate of online data, which is usually consensus and includes the whole population.

## Question 4:
The data was pretty dirty. We had to normalize the strings to lowercase, exclude specific rows, and figure out how to cut out irrelevant parts of the columns. We didn't threshold anything. Several values were missing, but there were no incomplete/partial rows. For some states, all of the data missing was because a state hadn't legalized sports betting yet. Yes, these missing rows contain essential information for our analysis, but we will restrict it to the data we do have and extrapolate it as a separate experiment. There were no duplicates in the data. Our data was skewed. Maine only has 3 rows, Kentucky has 4, Mass has 13, Ohio has 13, and Kansas has 17. Several states are completely missing, and all the rest have 24 or 25 rows. We didn't have any data type issues since we parsed everything into an int in Python while we were scraping. We threw away aggregate data since we can always reconstruct it. This should not affect any of our analyses.

# Population by state by year

## Question 1:
There are 1224 data points in this dataset. They are divided evenly across each state (+ DC). The year ranges from 2000 to 2023 (inclusive). (24*51 = 1224.) This should be enough to accurately predict the population for 2024 in every state. We are going to assume that the population of each state does not vary that much from month to month. So, we only need the data for each state by year.

## Question 2:
The identifying attributes of this data are the `year` and `state` pairs. The population varies based on those keys.

## Question 3:
We got the data from the Census Bureau. It came as a csv. The Census Bureau is perhaps the most reputable source possible. They've been doing data analysis for hundreds of years and are a branch of the government. It is a census, so the goal is to reach the entire population (so, in some sense, this isn't even sampling). It is likely to be biased towards upper-class people since they are more likely to have the time to fill it out and the resources to care about political representation.

## Question 4:
The data was provided as a csv. No data cleaning or thresholding was necessary. There were no missing values or duplicates. There were no data type issues. We didn't throw any data away. For this dataset, it did not make sense to analyze whether the data is uniform/skewed or for outliers since states will have varying populations due to external forces outside the parameters of this project. We examine the states with the highest and lowest average yearly growth rates, as growth rate will be pertinent to the goal of this table. The 5 states with the highest average yearly growth rates were: Nevada, Idaho, Utah, Texas, and Arizona. The 5 states with the lowest average yearly growth rates were Louisiana, Illinois, Indiana, Kansas, and Kentucky.


# Question 5: Summarize any challenges or observations you have made since collecting your data. Then, discuss your next steps and how your data collection has impacted the type of analysis you will perform. (approximately 3-5 sentences)

The data collection severely impacted the calculation we intended to perform. The lack of population data for 2024 made it a necessity to use the census data to estimate the 2024 population data. In addition, the lack of alcohol consumption data from 2022-2024 made it necessary to find the biggest alcohol dataset (the NIAAA dataset) to accurately estimate alcohol consumption by state from 2022-2024. Since our betting data is by month, and the alcohol consumption is by year, the retail sales data from FRED became necessary to accurately estimate alcohol consumption by state by month.