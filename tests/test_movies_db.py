from db_requester.db_helpers import DBHelper
from db_client import get_db_session


def test_movie_exists_in_db():

    session = get_db_session()

    db_helper = DBHelper(session)

    movie = db_helper.get_movie_by_id("44076")

    assert movie is not None