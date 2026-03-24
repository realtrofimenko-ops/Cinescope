class AuthAPI:
    def __init__(self, session):
        self.session = session
        self.base_url = "https://auth.dev-cinescope.coconutqa.ru"

    def login(self, email, password):
        return self.session.post(
            f"{self.base_url}/login",
            json={
                "email": email,
                "password": password
            }
        )