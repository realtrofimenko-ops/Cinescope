from custom_requester.custom_requester import CustomRequester


class MoviesAPI(CustomRequester):
    def __init__(self, session, base_url):
        super().__init__(session, base_url)

    def get_movies(self, params=None):
        return self.send_request("GET", "/movies", params=params)

    def get_movie_by_id(self, movie_id):
        return self.send_request("GET", f"/movies/{movie_id}")

    def create_movie(self, data):
        return self.send_request("POST", "/movies", json=data, expected_status=201)

    def update_movie(self, movie_id, data):
        return self.send_request("PATCH", f"/movies/{movie_id}", json=data)

    def delete_movie(self, movie_id):
        return self.send_request("DELETE", f"/movies/{movie_id}", expected_status=200)