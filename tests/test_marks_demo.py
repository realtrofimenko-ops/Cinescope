import pytest


@pytest.mark.ui
def test_ui_login_page():
    print("UI test")
    assert True


@pytest.mark.db
def test_db_connection():
    print("DB test")
    assert True


@pytest.mark.api
def test_api_dummy():
    print("API test")
    assert True