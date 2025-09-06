# Predict the probability of default, however the data input to the model is categorical 
    # -> so need to map 

# essentially a clustering optimisation algorithm

import pandas as pd
import numpy as np


def get_MSE(cluster_positions,mean_position):
    total_err2 = 0
    for cpos in cluster_positions:
        total_err2+=(cpos-mean_position)**2

    mse = total_err2/len(cluster_positions)

    return mse

def cluster_data(cluster_points,data_to_cluster):
    cluster_results = {}
    for data_val in data_to_cluster:
        data_val_position = np.searchsorted(cluster_points,data_val)

        if data_val_position == 0:
            cluster = cluster_points[0]

        elif data_val_position == len(cluster_points):
            cluster = cluster_points[-1]

        else:
            l_neighbour = cluster_points[data_val_position-1]
            h_neighbour = cluster_points[data_val_position]

            l_MSE = get_MSE([data_val],l_neighbour)
            h_MSE = get_MSE([data_val],h_neighbour)

            if l_MSE<h_MSE: #closer to the lower cluster point
                cluster = l_neighbour

            else:
                cluster = h_neighbour

        if cluster not in cluster_results:
            cluster_results[cluster] = []

        cluster_results[cluster].append(data_val)

#   return a dict with struct int(cluster position):[all values in cluster]
    return cluster_results

def getAverageMSE(clusters:dict[int,list[int]]):
    mse_total = 0
    for cluster_position in clusters:
        mse_total+=get_MSE(clusters[cluster_position],cluster_position)

    avg_mse = mse_total/len(clusters)

    return avg_mse

def getNewClusterPositions(clusters:dict[int,list[int]]):
    cluster_positions = []
    for cluster in clusters:
        datapoints = clusters[cluster]
        
        if len(datapoints)>0:
            new_position = sum(datapoints)/len(datapoints)
            cluster_positions.append(new_position)

        else:
            cluster_positions.append(cluster)            

    return cluster_positions

def getClusterBoundaries(final_cluster_positions):
    print(final_cluster_positions)
    cluster_boundaries = [300] #the lowest the FICO score can be
    for i in range(len(final_cluster_positions)-1):
        boundary = (final_cluster_positions[i]+final_cluster_positions[i+1])/2
        cluster_boundaries.append(int(boundary))

    cluster_boundaries.append(850)

    return cluster_boundaries



def cluster_optimisation(cluster_vals,n_buckets):
    cluster_vals = sorted(cluster_vals)
    cluster_points = np.sort(np.random.choice(cluster_vals, n_buckets, replace=False))
    mse_tolerance = 0.01

    clusters = cluster_data(cluster_points,cluster_vals)
    current_mse = getAverageMSE(clusters)

    while True:
        cluster_points = np.sort(getNewClusterPositions(clusters))
        clusters = cluster_data(cluster_points,cluster_vals)
        new_MSE = getAverageMSE(clusters)

        if (current_mse-new_MSE)/current_mse < mse_tolerance:
            print('Convergence Achieved')
            current_mse = new_MSE
            break

        current_mse = new_MSE

    final_cluster_positions = list(clusters.keys())

    cluster_boundaries = getClusterBoundaries(final_cluster_positions)

    print(f'Current Error: {round(np.sqrt(current_mse),3)}')
    for i in range(len(cluster_boundaries)-1):
        print(f'Boundary {i+1}: {cluster_boundaries[i]} -> {cluster_boundaries[i+1]}')




if __name__ == '__main__':
    #FICO Scores are 300-850

    loan_data = pd.read_csv('loan_data.csv')
    n_buckets = 10
    fico_scores = loan_data['fico_score'].to_numpy()
    boundaries = cluster_optimisation(fico_scores,n_buckets)





""" JPMorgan Chase & Co. Quantitative Research Virtual Experience Program on Forage - September 2025

 * Completed a simulation focused on quantitative research methods 
 * Analyzed a book of loans to estimate a customer's probability of default
 * Used dynamic programming to convert FICO scores into categorical data to
   predict defaults """