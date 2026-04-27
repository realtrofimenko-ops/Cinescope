import pytest
from models.user_model import RegisterUserResponse

pytestmark = pytest.mark.api


class TestUser:

    def test_create_user(self, super_admin, creation_user_data):
        response = super_admin.api.auth_api.register_user(creation_user_data)

        user = RegisterUserResponse(**response.json())

        assert user.email == creation_user_data.email


    def test_get_user_by_locator(self, super_admin, creation_user_data):
        created = RegisterUserResponse(
            **super_admin.api.auth_api.register_user(creation_user_data).json()
        )

        response_by_id = RegisterUserResponse(
            **super_admin.api.user_api.get_user(created.id).json()
        )

        response_by_email = RegisterUserResponse(
            **super_admin.api.user_api.get_user(creation_user_data.email).json()
        )

        assert response_by_id.email == response_by_email.email
        assert response_by_id.id == response_by_email.id
        assert response_by_id.fullName == creation_user_data.fullName


    @pytest.mark.slow
    def test_get_user_by_id_common_user(self, common_user):
        common_user.api.user_api.get_user(
            common_user.email,
            expected_status=403
        )