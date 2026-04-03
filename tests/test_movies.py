from utils.data_generator import DataGenerator


def test_get_movies(api_manager):
    response = api_manager.movies_api.get_movies()
    data = response.json()

    assert "movies" in data
    assert "count" in data
    assert isinstance(data["movies"], list)


def test_get_movie_by_id(api_manager, created_movie):
    movie_id = created_movie["id"]

    response = api_manager.movies_api.get_movie_by_id(movie_id)
    data = response.json()

    assert data["id"] == movie_id


def test_create_movie(api_manager):
    data = DataGenerator.generate_movie()

    response = api_manager.movies_api.create_movie(data)
    movie = response.json()

    assert "id" in movie
    assert movie["name"] == data["name"]

    api_manager.movies_api.delete_movie(movie["id"])


def test_update_movie(api_manager, created_movie):
    movie_id = created_movie["id"]

    update_data = DataGenerator.generate_movie()

    response = api_manager.movies_api.update_movie(movie_id, update_data)
    updated = response.json()

    assert updated["name"] == update_data["name"]


def test_delete_movie(api_manager):
    data = DataGenerator.generate_movie()

    create_response = api_manager.movies_api.create_movie(data)
    movie_id = create_response.json()["id"]

    api_manager.movies_api.delete_movie(movie_id)

    api_manager.movies_api.send_request(
        "GET",
        f"/movies/{movie_id}",
        expected_status=404
    )


def test_get_movies_with_filter(api_manager):
    params = {
        "genreId": 1
    }

    response = api_manager.movies_api.get_movies(params=params)
    data = response.json()

    assert "movies" in data

    for movie in data["movies"]:
        assert movie["genreId"] == 1