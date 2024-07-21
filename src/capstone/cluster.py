import sys
import sqlite3
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


def cluster(x_coord, y_coord, num_clusters, time_span):
    # connect to the all_data database
    conn = sqlite3.connect('data/data.db')
    c = conn.cursor()
    # turn this into a dataframe
    df = pd.read_sql_query("SELECT * FROM all_data", conn)
    if time_span == 'monthly':
        # group by state and find the mean of x_coord and y_coord
        df = df.groupby('state').mean()
        # get the x and y coordinates
        x = list(df[x_coord]/df['pop'])
        y = list(df[y_coord]/df['pop'])
    elif time_span == 'yearly':
        # group by state and year, and then take the yearly average of x_coord and y_coord
        df = df.groupby(['state', 'year']).mean()
        df = df.groupby('state').mean()
        # get the x and y coordinates
        x = list(df.groupby('state').mean()[x_coord])
        y = list(df.groupby('state').mean()[y_coord])

    coords = []
    for i in range(len(x)):
        coords.append([x[i], y[i]])
    
    coords = np.array(coords)
    kmeans = KMeans(n_clusters=num_clusters, n_init='auto')
    kmeans.fit(coords)
    y_kmeans = kmeans.predict(coords)
    # using y_kmeans, make a list of the states in each cluster
    clusters = []
    for i in range(num_clusters):
        clusters.append([])
    for i in range(len(y_kmeans)):
        clusters[y_kmeans[i]].append(df.index[i])


    df['cluster'] = y_kmeans+1
    df['state'] = df.index
    df['state_code'] = df['state']

    print(df.index)
    return df, clusters,  kmeans.cluster_centers_, y_kmeans

def main():
    # have main take 
    if sys.argv[1] == 'all':
        x_coords = ['wine', 'beer', 'spirits']
        y_coords = ['handle', 'gross_revenue', 'hold']
        num_clusters = [2, 3, 5]
        time_span = ['yearly', 'monthly']
        for x_coord in x_coords:
            for y_coord in y_coords:
                for num_cluster in num_clusters:
                    for span in time_span:
                        _, clusters, centers, y_kmeans = cluster(x_coord, y_coord, num_cluster, span)
                        print(clusters, centers)
                                # store the clusters in a json file
                        with open('data/clusters_json/' + span + '_' + str(num_cluster) + '_' + x_coord + '_' + y_coord + '_clusters.json', 'w') as f:
                            # write y_kmeans to the file
                            f.write('[')
                            for i in range(len(y_kmeans)):
                                f.write(str(y_kmeans[i]))
                                if i != len(y_kmeans) - 1:
                                    f.write(', ')
                            f.write(']')

    else:
        x_coord = sys.argv[1]
        y_coord = sys.argv[2]
        num_cluster = int(sys.argv[3])
        span = sys.argv[4]
        df, clusters, centers, _ = cluster(x_coord, y_coord, num_cluster, span)
        # go through each cluster and print the staes along with the cluster centers
        for i in range(len(clusters)):
            print('Cluster ' + str(i+1) + ':' + str(clusters[i]))
            print('Average ' + span + ' per Capita' + ' ' + x_coord + ' (Gallons): ' + str(centers[i][0]))
            print('Average ' + span + ' per Capita' + ' ' + y_coord + ' (Dollars): ' + str(centers[i][1]))

        # using plotly map all the clusters together with the states in each cluster
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
        df["state_code"] = df.index.map(state_abbreviations)
        fig1 = px.choropleth(df,
                             locations="state_code",
                             locationmode="USA-states",
                             color="cluster",
                             hover_name=df.index,
                             color_continuous_scale="Oranges",
                             labels={"cluster": "Cluster"},
                             scope="usa",
                             title="Clusters of States by Average" + x_coord + " Consumption and " + y_coord + " per Capita")
        fig1.show()
        
if __name__ == '__main__':
    main()
