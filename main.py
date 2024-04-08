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

    return (available_movies_genres[np.argmax(movies_similarities)]["filmname"], np.max(movies_similarities))

def has_watched_movies(person_name, ratings, filmname):
    return filmname in ratings["benutzername" == person_name]["filmname"]

def remove_watched_movies(person_name, ratings, genres):
    return genres[remove_watched_movies(person_name, ratings, genres["filmname"])]

def get_recommendation_generic(person_name, ratings, genres, historie, similarity_fn):
    watched_movies_names = historie[historie["benutzername"] == person_name]
    
    watched_movies_genres = genres[genres["filmname"] in watched_movies_names["filmname"]]
    available_movies_genres = genres["filmname"] not in watched_movies_names["filmname"]

    if len(available_movies_genres) == 0:
        return get_generic_recommendations(ratings, genres, historie)

    movie, rating = get_most_similar(watched_movies_genres, available_movies_genres, lambda m_avg, m_option: similarity_fn(m_avg, m_option))
    return (movie, rating)

def get_recommendation_generic_with_rating(person_name, ratings, genres, historie, similarity_fn):
    raise NotImplementedError("Not implemented yet")

def get_generic_recommendations(ratings, genres, historie):
    raise NotImplementedError("Not implemented yet")

def get_recommendation_by_dotproduct(person_name, ratings, genres, historie):
    return get_recommendation_generic(person_name, ratings, genres, historie, lambda m_avg, m_option: np.dot(m_avg, m_option))

def get_recommendation_by_dotproduct_with_rating(person_name, ratings, genres, historie):
    return get_recommendation_generic_with_rating(person_name, ratings, genres, historie, lambda m_avg, m_option: np.dot(m_avg, m_option))


if __name__ == "__main__":
    print(get_recommendation_by_dotproduct("hans", ratings, genres, historie))