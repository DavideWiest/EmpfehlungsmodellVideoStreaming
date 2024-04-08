import numpy as np
import pandas


class Data():
    def __init__(self, genres, historie, ratings):
        self.genres = genres
        self.historie = historie
        self.ratings = ratings

        for column in self.genres.columns:
            if column == "filmname": continue
            self.genres[column] = self.genres[column].astype(float)
        for column in self.ratings.columns:
            if column == " filmname" or column == "benutzername": continue
            self.ratings[column] = self.ratings[column].astype(float)

        self.ratings["filmname"] = self.ratings[" filmname"]
        del self.ratings[" filmname"]

        self.ratings["bewertung"] = self.ratings[" bewertung"]
        del self.ratings[" bewertung"]
        
        for movie_name in self.ratings["filmname"]:
            # strip the movie name string
            self.ratings["filmname"] = self.ratings["filmname"].replace(movie_name, movie_name.strip())


class PersonData():
    def __init__(self, person_name, data):
        self.person_name = person_name
        
        self.watched_movies_names = data.genres[data.ratings["benutzername"] == person_name]["filmname"].values
        self.watched_movies_genres = data.genres[data.genres["filmname"].isin(self.watched_movies_names)]
        self.available_movies_genres = data.genres[data.genres["filmname"].isin(self.watched_movies_names) == False]

class UserProfileAlg():
    def __init__(self, rating, avg_rating, time):
        self.rating = rating
        self.avg_rating = avg_rating
        self.time = time

    def similarity_fn(self, m_avg, m_option):
        return np.dot(m_avg, m_option)  # Transpose the m_option array to align dimensions properly
    
    def get_movie_profile(self, data, person_data):
        if self.rating:
            raise NotImplementedError("Not implemented yet")
        if self.avg_rating:
            raise NotImplementedError("Not implemented yet")
        if self.time:
            raise NotImplementedError("Not implemented yet")

        params = person_data.watched_movies_genres
        del params["filmname"]
        return np.mean(params, axis=0)

    def get_most_similar(self, movies_genres_avg, data: Data, person_data: PersonData):
        movies_similarities = []
        for movie in person_data.available_movies_genres["filmname"]:
            # remove the movie name
            params_movie = person_data.available_movies_genres[person_data.available_movies_genres["filmname"] == movie]
            del params_movie["filmname"]
            movies_similarities.append(self.similarity_fn(movies_genres_avg, params_movie.T))

        movie = person_data.available_movies_genres.iloc[np.argmax(np.array(movies_similarities))]["filmname"]
        return (movie, np.max(movies_similarities))

    def get_recommendation(self, data: Data, person_data: PersonData):
        if len(person_data.watched_movies_genres) == 0:
            return self.get_generic_recommendations(data, person_data)

        m_avg = self.get_movie_profile(data, person_data)
        return self.get_most_similar(m_avg, data, person_data)

    def get_generic_recommendations(self, data, person_data):
        ratings = []
        for movie in person_data.available_movies_genres["filmname"]:
            avg_rating = np.mean(data.ratings[data.ratings["filmname"] == movie]["bewertung"])
            ratings.append(avg_rating)

        max_rating = 5
        return (data.ratings["filmname"].iloc[np.argmax(avg_rating)], avg_rating / max_rating)


if __name__ == "__main__":
    
    genres = pandas.read_csv('in/streaming_genres.csv', delimiter=',', header=0)
    historie = pandas.read_csv('in/streaming_historie.csv', delimiter=',', header=0)
    ratings = pandas.read_csv('in/streaming_ratings.csv', delimiter=',', header=0)

    data = Data(genres, historie, ratings)
    person_data = PersonData("asdf", data)

    alg = UserProfileAlg(False, False, False)

    print(alg.get_recommendation(data, person_data))