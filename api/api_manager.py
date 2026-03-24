# tests/api/api_manager.py

from .auth_api import AuthAPI
from .movies_api import MoviesAPI


class ApiManager:
    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url

        self.auth_api = AuthAPI(session)
        self.movies_api = MoviesAPI(session, base_url)