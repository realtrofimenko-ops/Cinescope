from sqlalchemy.orm import Session

from db_models.user import UserDBModel
from db_models.movies import MovieDBModel




class DBHelper:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_user_by_id(self, user_id: str):
        return (
            self.db_session
            .query(UserDBModel)
            .filter(UserDBModel.id == user_id)
            .first()
        )

    def get_user_by_email(self, email: str):
        return (
            self.db_session
            .query(UserDBModel)
            .filter(UserDBModel.email == email)
            .first()
        )

    def user_exists_by_email(self, email: str) -> bool:
        return (
            self.db_session
            .query(UserDBModel)
            .filter(UserDBModel.email == email)
            .count() > 0
        )

    def get_movie_by_name(self, name: str):
        return (
            self.db_session
            .query(MovieDBModel)
            .filter(MovieDBModel.name == name)
            .first()
        )

    def create_test_user(self, user_data: dict):
        user = UserDBModel(**user_data)

        self.db_session.add(user)

        self.db_session.commit()

        self.db_session.refresh(user)

        return user

    def delete_user(self, user):
        self.db_session.delete(user)

        self.db_session.commit()

    def get_movie_by_id(self, movie_id: str):
        return self.db_session.query(MovieDBModel).filter(
            MovieDBModel.id == movie_id
        ).first()

    def get_movie_by_name(self, movie_name: str):
        return self.db_session.query(MovieDBModel).filter(
            MovieDBModel.name == movie_name
        ).first()