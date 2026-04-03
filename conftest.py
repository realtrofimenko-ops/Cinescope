import pytest
import requests
from clients.api_manager import ApiManager
from clients.auth_api import AuthAPI

API_URL = "https://api.dev-cinescope.coconutqa.ru"


@pytest.fixture(scope="session")
def session():
    return requests.Session()


@pytest.fixture(scope="session")
def api_manager(session):
    auth_api = AuthAPI(session)

    response = auth_api.login(
        email="api1@gmail.com",
        password="asdqwe123Q"
    )

    token = response.json()["accessToken"]

    session.headers.update({
        "Authorization": f"Bearer {token}"
    })

    return ApiManager(session, API_URL)


@pytest.fixture
def created_movie(api_manager):
    from utils.data_generator import DataGenerator

    data = DataGenerator.generate_movie()

    response = api_manager.movies_api.create_movie(data)
    movie = response.json()

    yield movie

    api_manager.movies_api.delete_movie(movie["id"])