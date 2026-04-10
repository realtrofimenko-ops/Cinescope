import logging

logger = logging.getLogger(__name__)


class CustomRequester:

    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url

    def send_request(self, method, endpoint, expected_status=200, **kwargs):
        url = f"{self.base_url}{endpoint}"

        logger.info(f"{method} {url}")
        response = self.session.request(method, url, **kwargs)
        logger.info(f"Response: {response.status_code} {response.text}")

        assert response.status_code == expected_status, \
            f"Expected {expected_status}, got {response.status_code}: {response.text}"

        return response