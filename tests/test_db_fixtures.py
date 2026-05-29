def test_db_requests(db_helper, created_test_user):

    user_from_db = db_helper.get_user_by_id(
        created_test_user.id
    )

    assert user_from_db is not None

    assert user_from_db.email == created_test_user.email