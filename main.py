import numpy as np
import pandas

genres = pandas.read_csv('in/streaming_genres.csv', dtype=np.int32, delimiter=',', header=0)
historie = pandas.read_csv('in/streaming_historie.csv', dtype=np.int32, delimiter=',', header=0)
ratings = pandas.read_csv('in/streaming_ratings.csv', dtype=np.int32, delimiter=',', header=0)

def get_most_similar(movies_genres, available_movies):
    movies_avg = np.mean(movies_genres, axis=0)
    most_similar_movie = available_movies.sort