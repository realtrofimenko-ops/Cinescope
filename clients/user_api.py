from custom_requester.custom_requester import CustomRequester


class UserApi(CustomRequester):
    USER_BASE_URL = "https://auth.dev-cinescope.coconutqa.ru"

    def __init__(self, session):
        super().__init__(session, self.USER_BASE_URL)

    def get_user(self, user_locator, expected_status=200):
        return self.send_request(
            method="GET",
            endpoint=f"/user/{user_locator}",
            expected_status=expected_status
        )