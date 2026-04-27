from clients.movies_api import MoviesAPI
from clients.auth_api import AuthAPI
from clients.user_api import UserApi


class ApiManager:

    def __init__(self, session, base_url):
        self.movies_api = MoviesAPI(session, base_url)
        self.auth_api = AuthAPI(session)
        self.user_api = UserApi(session)