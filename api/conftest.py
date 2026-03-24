import pytest
import requests
from .api_manager import ApiManager
from .auth_api import AuthAPI
from .data_generator import DataGenerator

API_URL = "https://api.dev-cinescope.coconutqa.ru"


@pytest.fixture
def api_manager():
    session = requests.Session()

    auth_api = AuthAPI(session)

    # 🔐 логин
    response = auth_api.login(
        email="api1@gmail.com",
        password="asdqwe123Q"
    )

    assert response.status_code == 200, f"Login failed: {response.text}"

    data = response.json()
    token = data.get("accessToken")

    assert token is not None, f"No token in response: {response.text}"

    session.headers.update({
        "Authorization": f"Bearer {token}"
    })

    return ApiManager(session, API_URL)


@pytest.fixture
def created_movie(api_manager):
    data = DataGenerator.generate_movie()

    response = api_manager.movies_api.create_movie(data)
    assert response.status_code == 201, f"Create failed: {response.text}"

    movie = response.json()

    yield movie

    # 🧹 cleanup
    api_manager.movies_api.delete_movie(movie["id"])