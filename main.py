import numpy as np
import pandas

genres = pandas.read_csv('in/streaming_genres.csv', dtype=np.int32, delimiter=',', header=0)
historie = pandas.read_csv('in/streaming_historie.csv', dtype=np.int32, delimiter=',', header=0)
ratings = pandas.read_csv('in/streaming_ratings.csv', dtype=np.int32, delimiter=',', header=0)

def get_most_similar(watched_movies_genres, available_movies_genres, similarity_fn):
    movies_avg = np.mean(watched_movies_genres, axis=0)
    movies_similarities = []
    for movie in available_movies_genres:
        # remove the movie name
        params_movie = watched_movies_genres[movie][1:]
        movies_similarities.append(similarity_fn(movies_avg, params_movie))

    return available_movies_genres[np.argmax(movies_similarities)]["filmname"]

def has_watched_movies(person_name, ratings, filmname):
    return filmname in ratings["benutzername" == person_name]["filmname"]

def remove_watched_movies(person_name, ratings, genres):
    return genres[remove_watched_movies(person_name, ratings, genres["filmname"])]

def get_recommendation_by_dotproduct(person_name, ratings, genres, historie):
    watched_movies_names = historie[historie["benutzername"] == person_name]
    
    watched_movies_genres = genres[genres["filmname"] in watched_movies_names["filmname"]]
    available_movies_genres = genres["filmname"] not in watched_movies_names["filmname"]

    movie = get_most_similar(watched_movies_genres, available_movies_genres, lambda x,y: np.dot(x, y))
    return movie

if __name__ == "__main__":
    print(get_recommendation_by_dotproduct("hans", ratings, genres, historie))