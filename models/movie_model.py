from pydantic import BaseModel
from typing import List, Optional


class MovieModel(BaseModel):
    id: int
    name: str
    description: Optional[str] = None


class MoviesResponseModel(BaseModel):
    movies: List[MovieModel]
    count: int
    page: int
    pageSize: int
    pageCount: int