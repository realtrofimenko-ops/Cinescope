import random


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