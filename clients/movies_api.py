from custom_requester.custom_requester import CustomRequester


class MoviesAPI(CustomRequester):

    def get_movies(self, params=None, expected_status=200):
        return self.send_request(
            "GET",
            "/movies",
            params=params,
            expected_status=expected_status
        )

    def get_movie_by_id(self, movie_id, expected_status=200):
        return self.send_request(
            "GET",
            f"/movies/{movie_id}",
            expected_status=expected_status
        )

    def create_movie(self, data, expected_status=201):
        return self.send_request(
            "POST",
            "/movies",
            json=data,
            expected_status=expected_status
        )

    def update_movie(self, movie_id, data, expected_status=200):
        return self.send_request(
            "PATCH",
            f"/movies/{movie_id}",
            json=data,
            expected_status=expected_status
        )

    def delete_movie(self, movie_id, expected_status=200):
        return self.send_request(
            "DELETE",
            f"/movies/{movie_id}",
            expected_status=expected_status
        )