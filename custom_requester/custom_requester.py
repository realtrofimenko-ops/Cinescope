import logging
from pydantic import BaseModel
import json

logger = logging.getLogger(__name__)


class CustomRequester:

    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url

    def send_request(self, method, endpoint, expected_status=200, **kwargs):
        url = f"{self.base_url}{endpoint}"

        logger.info(f"{method} {url}")

        data = kwargs.get("json")

        if isinstance(data, BaseModel):
            kwargs["json"] = data.model_dump()

        response = self.session.request(method, url, **kwargs)

        assert response.status_code == expected_status

        return response