import psycopg2
from resources.db_creds import DBCreds


def test_db_connection():
    try:
        connection = psycopg2.connect(
            host=DBCreds.HOST,
            port=DBCreds.PORT,
            database=DBCreds.NAME,
            user=DBCreds.USER,
            password=DBCreds.PASSWORD
        )

        cursor = connection.cursor()

        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()

        print("Connected to PostgreSQL!")
        print("Version:", db_version)

        cursor.close()
        connection.close()

    except Exception as e:
        print("Ошибка подключения к БД:", e)
if __name__ == "__main__":
    test_db_connection()