from custom_requester.custom_requester import CustomRequester


class AuthAPI(CustomRequester):
    def __init__(self, session):
        super().__init__(session, "https://auth.dev-cinescope.coconutqa.ru")

    def login(self, email, password):
        return self.send_request(
            "POST",
            "/login",
            json={
                "email": email,
                "password": password
            }
        )