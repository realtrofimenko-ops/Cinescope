import requests

from unittest.mock import Mock
from pydantic import BaseModel


class DateTimeRequest(BaseModel):
    currentDateTime: str


class WhatIsTodayResponse(BaseModel):
    message: str


def get_worldclockap_time():
    response = requests.get(
        "http://worldclockapi.com/api/json/utc/now"
    )

    assert response.status_code == 200

    return response.json()

def stub_get_worldclockap_time():

    class StubResponse:
        def __init__(self):
            self.currentDateTime = "2025-05-09T00:00Z"

    return StubResponse()


def test_what_is_today_BY_MOCK(mocker):

    # создаем фейковый response
    fake_response = Mock()

    # что вернет response.status_code
    fake_response.status_code = 200

    # что вернет response.json()
    fake_response.json.return_value = {
        "currentDateTime": "2025-01-01T00:00Z"
    }

    # мокируем requests.get
    mocker.patch(
        "requests.get",
        return_value=fake_response
    )

    # теперь реального запроса НЕ будет
    world_clock_response = get_worldclockap_time()

    # запрос в локальный сервис
    what_is_today_response = requests.post(
        "http://127.0.0.1:16002/what_is_today",
        json={
            "currentDateTime": world_clock_response["currentDateTime"]
        }
    )

    # проверки
    assert what_is_today_response.status_code == 200

    response_json = what_is_today_response.json()

    assert response_json["message"] == "Новый год"

def test_what_is_today_BY_STUB(monkeypatch):

    # подменяем настоящую функцию на stub
    monkeypatch.setattr(
        "tests.test_mock_services.get_worldclockap_time",
        stub_get_worldclockap_time
    )

    # вызываем stub напрямую
    world_clock_response = stub_get_worldclockap_time()

    # отправляем запрос в локальный сервис
    what_is_today_response = requests.post(
        "http://127.0.0.1:16002/what_is_today",
        json={
            "currentDateTime": world_clock_response.currentDateTime
        }
    )

    # проверки
    assert what_is_today_response.status_code == 200

    response_json = what_is_today_response.json()

    assert response_json["message"] == "День Победы"