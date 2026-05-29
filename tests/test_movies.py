import datetime
import random

import allure
import pytest

from utils.data_generator import DataGenerator
from db_client import get_db_session
from db_models.movies import MovieDBModel
from db_requester.db_helpers import DBHelper
from models.movie_model import MoviesResponseModel

pytestmark = pytest.mark.api

@allure.epic("Movies")
@allure.feature("Movies list")
@allure.story("Получение списка фильмов")
@allure.title("Проверка получения списка фильмов")
@pytest.mark.smoke
@pytest.mark.slow
def test_get_movies(api_manager):

    with allure.step("Отправляем запрос на получение фильмов"):
        response = api_manager.movies_api.get_movies()

    with allure.step("Проверяем статус код"):
        assert response.status_code == 200

    with allure.step("Проверяем pydantic модель"):
        data = MoviesResponseModel(**response.json())

    with allure.step("Проверяем структуру ответа"):
        assert isinstance(data.movies, list)
        assert data.count >= 0
        assert data.page >= 1


@allure.epic("Movies")
@allure.feature("Movie by id")
@allure.story("Получение фильма")
@allure.title("Проверка фильма по id")
@pytest.mark.regression
def test_get_movie_by_id(api_manager, created_movie):

    movie_id = created_movie

    with allure.step(f"Получаем фильм с id {movie_id}"):
        response = api_manager.movies_api.get_movie_by_id(movie_id)

    with allure.step("Проверяем статус код"):
        assert response.status_code == 200

    with allure.step("Проверяем id фильма"):
        data = response.json()
        assert data["id"] == movie_id


@allure.epic("Movies")
@allure.feature("Create movie")
@allure.story("Создание фильма")
@allure.title("Проверка создания фильма")
@pytest.mark.smoke
def test_create_movie(api_manager):

    with allure.step("Генерируем данные фильма"):
        data = DataGenerator.generate_movie()

    with allure.step("Создаем фильм"):
        response = api_manager.movies_api.create_movie(data)

    with allure.step("Проверяем статус код"):
        assert response.status_code == 201

    with allure.step("Проверяем тело ответа"):
        movie = response.json()

        assert "id" in movie
        assert movie["name"] == data["name"]

    with allure.step("Удаляем тестовый фильм"):
        api_manager.movies_api.delete_movie(movie["id"])


def test_update_movie(api_manager, created_movie):
    movie_id = created_movie

    update_data = DataGenerator.generate_movie()

    response = api_manager.movies_api.update_movie(movie_id, update_data)
    updated = response.json()

    assert updated["name"] == update_data["name"]

@allure.epic("Movies")
@allure.feature("Delete movie")
@allure.story("Удаление фильма")
@allure.title("Проверка удаления фильма")
@pytest.mark.db
@pytest.mark.regression
def test_delete_movie(api_manager, super_admin):

    session = get_db_session()

    db_helper = DBHelper(session)

    movie_id = random.randint(10000, 99999)

    # Проверяем есть ли фильм в БД
    movie = db_helper.get_movie_by_id(movie_id)

    # Если фильма нет — создаем
    if movie is None:
        movie = MovieDBModel(
            id=movie_id,
            name=f"Test Movie {random.randint(1, 999999)}",
            price=100,
            description="Test description",
            image_url="https://test.com/image.jpg",
            location="SPB",
            published=True,
            rating=5.0,
            genre_id=1,
            created_at=datetime.datetime.now()
        )

        session.add(movie)
        session.commit()

    # Проверяем что фильм существует
    movie = db_helper.get_movie_by_id(movie_id)

    assert movie is not None

    # Удаляем через API
    delete_response = api_manager.movies_api.delete_movie(
        movie_id=movie_id
    )

    assert delete_response.status_code == 200

    # Проверяем что фильм удалился из БД
    deleted_movie = db_helper.get_movie_by_id(movie_id)

    assert deleted_movie is None


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


@pytest.mark.parametrize(
    "params, check_func",
    [
        (
            {"minPrice": 10, "maxPrice": 100},
            lambda movie: 10 <= movie["price"] <= 100
        ),
        (
            {"locations": ["MSK"]},
            lambda movie: movie["location"] == "MSK"
        ),
        (
            {"genreId": 1},
            lambda movie: movie["genreId"] == 1
        ),
    ],
    ids=[
        "filter_by_price",
        "filter_by_location",
        "filter_by_genre"
    ]
)
def test_get_movies_with_filters_parametrized(api_manager, params, check_func):
    response = api_manager.movies_api.get_movies(params=params)
    data = response.json()

    assert "movies" in data, "Ответ должен содержать список movies"

    movies = data["movies"]

    # если вдруг пусто — это не ошибка фильтра
    if not movies:
        pytest.skip("Нет фильмов для данного фильтра")

    for movie in movies:
        assert check_func(movie), f"Фильм не соответствует фильтру: {movie}"
@pytest.mark.parametrize(
    "user_fixture, expected_status",
    [
        ("super_admin", 200),
        ("admin_user", 403),
        ("common_user", 403),
    ],
    ids=[
        "super_admin_can_delete",
        "admin_cannot_delete",
        "user_cannot_delete"
    ]
)
@pytest.mark.slow
def test_delete_movie_by_roles(request, user_fixture, expected_status, created_movie, super_admin):
    user = request.getfixturevalue(user_fixture)

    movie_id = created_movie

    response = user.api.movies_api.delete_movie(
        movie_id,
        expected_status=expected_status
    )

    print("STATUS:", response.status_code)
    print("BODY:", response.text)

    # ✅ проверяем через супер-админа
    if expected_status == 200:
        super_admin.api.movies_api.get_movie_by_id(movie_id, expected_status=404)