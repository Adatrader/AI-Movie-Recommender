# Filename: svd.py
# Authors: David Allison, Minh Huynh
# Description: SVD implementation for movie recommendations
# Tested on: py-3.8.6 && kivy-2.0.0rc4

import numpy as np

# SVD method of getting movie recommendations
def SVD(movie_index, num_recommendations, data_n):

    movie_ids = []
    for key in data_n:
        movie_ids.append(key)

    data_mat = data_n.to_numpy().T
    #print(data_mat)
    mean_m= np.asarray([(np.mean(data_mat, 1))]).T
    #print(mean_m)
    normalised_mat = data_mat - mean_m

    A = normalised_mat.T / np.sqrt(data_mat.shape[0] - 1)
    U, S, V = np.linalg.svd(A)

    def top_cosine_similarity(data_n, movie_id, top_n=10):
        index = movie_id - 1 # Movie id starts from 1 in the dataset
        movie_row = data_n[index, :]
        magnitude = np.sqrt(np.einsum('ij, ij -> i', data_n, data_n))
        similarity = np.dot(movie_row, data_n.T) / (magnitude[index] * magnitude)
        sort_indexes = np.argsort(-similarity)
        return sort_indexes[:top_n]

    #k-principal components to represent movies
    k = 50
    sliced = V.T[:, :k] # representative data
    indexes = top_cosine_similarity(sliced, movie_index, num_recommendations)

    recommended_ids = []
    for key in indexes:
        recommended_ids.append(movie_ids[key])

    return recommended_ids
