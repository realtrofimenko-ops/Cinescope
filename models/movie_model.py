from pydantic import BaseModel
from typing import List, Optional


class GenreModel(BaseModel):
    name: str


class MovieModel(BaseModel):
    id: int
    name: str
    price: int
    description: str
    imageUrl: Optional[str] = None
    location: str
    published: bool
    rating: float
    genreId: int
    createdAt: str
    genre: GenreModel


class MoviesResponseModel(BaseModel):
    movies: List[MovieModel]
    count: int
    page: int
    pageSize: int
    pageCount: int