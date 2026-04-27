import json
from models.user_model import UserModel


def test_pydantic_user_models(test_user, creation_user_data):

    user1 = test_user
    user2 = creation_user_data

    json_user1 = user1.model_dump(exclude_unset=True, mode="json")
    json_user2 = user2.model_dump(mode="json")

    print("\nTEST_USER JSON (exclude_unset=True):")
    print(json.dumps(json_user1, indent=2, ensure_ascii=False))

    print("\nCREATION_USER_DATA JSON:")
    print(json.dumps(json_user2, indent=2, ensure_ascii=False))