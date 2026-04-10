from utils.data_generator import DataGenerator


def test_get_movies(api_manager):
    response = api_manager.movies_api.get_movies()
    data = response.json()

    assert "movies" in data
    assert "count" in data
    assert isinstance(data["movies"], list)
    assert "page" in data
    assert "pageSize" in data
    assert "pageCount" in data


def test_get_movie_by_id(api_manager, created_movie):
    movie_id = created_movie

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
    movie_id = created_movie

    update_data = DataGenerator.generate_movie()

    response = api_manager.movies_api.update_movie(movie_id, update_data)
    updated = response.json()

    assert updated["name"] == update_data["name"]


def test_delete_movie(api_manager, created_movie):
    movie_id = created_movie

    api_manager.movies_api.delete_movie(movie_id)

    # проверка
    api_manager.movies_api.get_movie_by_id(
        movie_id,
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

def test_create_movie_invalid_data(api_manager):
    data = {
        "name": "",  # пустое имя
    }

    response = api_manager.movies_api.create_movie(
        data,
        expected_status=400
    )

    assert response.status_code == 400

def test_get_movie_not_found(api_manager):
    fake_id = 999999999

    response = api_manager.movies_api.get_movie_by_id(
        fake_id,
        expected_status=404
    )

    assert response.status_code == 404