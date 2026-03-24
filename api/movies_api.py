from .custom_requester import CustomRequester


class MoviesAPI:
    def __init__(self, session, base_url):
        self.requester = CustomRequester(session)
        self.base_url = f"{base_url}/movies"

    def get_movies(self, params=None):
        return self.requester.get(self.base_url, params=params)

    def create_movie(self, data):
        return self.requester.post(self.base_url, json=data)

    def update_movie(self, movie_id, data):
        return self.requester.patch(f"{self.base_url}/{movie_id}", json=data)

    def delete_movie(self, movie_id):
        return self.requester.delete(f"{self.base_url}/{movie_id}")