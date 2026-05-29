from db_client import get_db_session
from db_requester.db_helpers import DBHelper


def test_get_user_by_id():

    session = get_db_session()

    db_helper = DBHelper(session)

    user = db_helper.get_user_by_id(
        "995c7fa5-34b3-4f48-93a6-ffbf7b6dd360"
    )

    assert user is not None
    assert user.id == "995c7fa5-34b3-4f48-93a6-ffbf7b6dd360"

    session.close()