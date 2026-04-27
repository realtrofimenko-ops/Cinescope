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

    def authenticate(self, creds):
        email, password = creds

        response = self.send_request(
            method="POST",
            endpoint="/login",
            json={
                "email": email,
                "password": password
            },
            expected_status=200
        )

        token = response.json().get("accessToken")

        self.session.headers.update({
            "Authorization": f"Bearer {token}"
        })

        return response

    def register_user(self, user_model):
        data = user_model.model_dump(mode="json")

        # ❗ УДАЛЯЕМ лишние поля
        data.pop("roles", None)
        data.pop("verified", None)
        data.pop("banned", None)

        return self.send_request(
            "POST",
            "/register",
            expected_status=201,  # ← ВАЖНО (у тебя уже почти правильно)
            json=data
        )