import pytest
import requests

from clients.api_manager import ApiManager
from clients.auth_api import AuthAPI
from utils.constants import EMAIL, PASSWORD, BASE_URL
from entities.user import User
from utils.data_generator import DataGenerator
from utils.roles import Roles
from utils.user_creds import SuperAdminCreds
from models.user_model import UserModel


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
SUPER_ADMIN_EMAIL = EMAIL
SUPER_ADMIN_PASSWORD = PASSWORD


@pytest.fixture(scope="session")
def super_admin(api_manager):
    user = User(
        email=SuperAdminCreds.USERNAME,
        password=SuperAdminCreds.PASSWORD,
        roles=[Roles.SUPER_ADMIN.value],
        api=api_manager
    )
    return user
@pytest.fixture
def test_user() -> UserModel:
    password = DataGenerator.generate_random_password()

    return UserModel(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=password,
        passwordRepeat=password,
        roles=[Roles.USER]
    )
@pytest.fixture
def creation_user_data(test_user: UserModel) -> UserModel:
    data = test_user.model_dump()

    data["verified"] = True
    data["banned"] = False

    return UserModel(**data)

@pytest.fixture(scope="session")
def user_session():
    def _create_session():
        return requests.Session()
    return _create_session
@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    from clients.api_manager import ApiManager
    new_api_manager = ApiManager(new_session, BASE_URL)

    user = User(
        creation_user_data.email,
        creation_user_data.password,
        [Roles.USER.value],  # ← ИСПРАВЛЕНО
        new_api_manager
    )

    super_admin.api.auth_api.register_user(creation_user_data)
    user.api.auth_api.authenticate(user.creds)

    return user
@pytest.fixture
def admin_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    from clients.api_manager import ApiManager
    from utils.constants import BASE_URL

    new_api_manager = ApiManager(new_session, BASE_URL)

    admin = User(
        creation_user_data.email,
        creation_user_data.password,
        [Roles.ADMIN.value],
        new_api_manager
    )

    # создаём пользователя через супер-админа
    creation_user_data = creation_user_data.model_copy(
        update={"roles": [Roles.ADMIN]}
    )
    super_admin.api.auth_api.register_user(creation_user_data)

    # логинимся
    admin.api.auth_api.authenticate(admin.creds)

    return admin
@pytest.fixture
def print_hello():
    print("\nHELLO FROM FIXTURE")
@pytest.mark.usefixtures("print_hello")
def test_usefixtures_example():
    assert True