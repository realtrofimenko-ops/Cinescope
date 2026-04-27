from clients.api_manager import ApiManager


class User:
    def __init__(self, email: str, password: str, roles: list, api: ApiManager):
        self.email = email
        self.password = password
        self.roles = roles
        self.api = api  # 🔥 теперь пользователь умеет делать запросы

    @property
    def creds(self):
        """Удобно доставать email и пароль"""
        return self.email, self.password