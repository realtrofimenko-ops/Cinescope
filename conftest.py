import pytest
import requests

from clients.api_manager import ApiManager
from clients.auth_api import AuthAPI
from utils.constants import EMAIL, PASSWORD, BASE_URL


@pytest.fixture(scope="session")
def session():
    return requests.Session()


@pytest.fixture(scope="session")
def api_manager(session):
    auth_api = AuthAPI(session)

    response = auth_api.login(EMAIL, PASSWORD)
    token = response.json()["accessToken"]

    session.headers.update({
        "Authorization": f"Bearer {token}"
    })

    return ApiManager(session, BASE_URL)


@pytest.fixture
def created_movie(api_manager):
    from utils.data_generator import DataGenerator

    data = DataGenerator.generate_movie()

    response = api_manager.movies_api.create_movie(data)
    movie_id = response.json()["id"]

    yield movie_id

    # безопасное удаление
    try:
        api_manager.movies_api.delete_movie(movie_id)
    except AssertionError:
        # если уже удалён — ок
        pass