from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from resources.db_creds import DBCreds


USERNAME = DBCreds.USER
PASSWORD = DBCreds.PASSWORD
HOST = DBCreds.HOST
PORT = DBCreds.PORT
DATABASE_NAME = DBCreds.NAME


engine = create_engine(
    f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}",
    echo=False
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db_session():
    return SessionLocal()


def test_connection():

    with engine.connect() as connection:

        result = connection.execute(text("SELECT version();"))

        for row in result:
            print("SQLAlchemy connected!")
            print("Version:", row)


if __name__ == "__main__":
    test_connection()