import random
from faker import Faker
import string
import time
import datetime
from uuid import uuid4

fake = Faker()

class DataGenerator:
    @staticmethod
    def generate_movie():
        return {
            "name": f"Test Movie {random.randint(1, 999999)}",
            "imageUrl": "https://example.com/image.png",
            "price": random.randint(1, 1000),
            "description": "Test Description",
            "location": "MSK",
            "published": True,
            "genreId": 1
        }

    @staticmethod
    def generate_user():
        password = "Test1234Aa"

        return {
            "email": fake.email(),
            "fullName": fake.name(),
            "password": password,
            "roles": ["USER"]
        }

    @staticmethod
    def generate_random_password(length=10):
        letters = string.ascii_letters
        digits = string.digits
        return ''.join(random.choice(letters + digits) for _ in range(length))

    @staticmethod
    def generate_random_email():
        return f"{fake.email()}"

    @staticmethod
    def generate_random_name():
        return fake.name()

    @staticmethod
    def generate_user_data():
        return {
            'id': f'{uuid4()}',
            'email': DataGenerator.generate_random_email(),
            'full_name': DataGenerator.generate_random_name(),
            'password': DataGenerator.generate_random_password(),
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now(),
            'verified': False,
            'banned': False,
            'roles': '{USER}'
        }