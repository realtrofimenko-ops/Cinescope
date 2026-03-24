import requests
from .data_generator import DataGenerator

API_URL = "https://api.dev-cinescope.coconutqa.ru"


# 🟢 GET список фильмов
def test_get_movies(api_manager):
    response = api_manager.movies_api.get_movies()

    assert response.status_code == 200


# 🟢 CREATE фильм
def test_create_movie(api_manager):
    data = DataGenerator.generate_movie()

    response = api_manager.movies_api.create_movie(data)

    assert response.status_code == 201


# 🟢 UPDATE фильм
def test_update_movie(api_manager, created_movie):
    movie_id = created_movie["id"]

    update_data = {
        "name": "Updated Movie",
        "price": 999,
        "description": "Updated Description",
        "location": "SPB",
        "imageUrl": "https://example.com/new.png",
        "published": True,
        "genreId": 1
    }

    response = api_manager.movies_api.update_movie(movie_id, update_data)

    assert response.status_code == 200


# 🔴 NEGATIVE: без авторизации
def test_create_movie_unauthorized():
    response = requests.post(
        f"{API_URL}/movies",
        json={}
    )

    assert response.status_code == 401


# 🔴 NEGATIVE: невалидные данные
def test_create_movie_invalid_data(api_manager):
    response = api_manager.movies_api.create_movie({})

    assert response.status_code == 400


# 🔍 ФИЛЬТР (обязательный)
def test_get_movies_with_filter(api_manager):
    params = {
        "page": 1,
        "pageSize": 5
    }

    response = api_manager.movies_api.get_movies(params=params)

    assert response.status_code == 200

    data = response.json()

    # универсальная проверка
    assert isinstance(data, list) or "movies" in data