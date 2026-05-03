from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional

class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    year: int = Field(..., ge=1000, le=2026)
    author_id: int

class BookResponse(BaseModel):
    id: int
    title: str
    year: int
    author_id: int
    model_config = ConfigDict(from_attributes=True)

class AuthorCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)

class ReviewCreate(BaseModel):
    book_id: int
    rating: float = Field(..., ge=1.0, le=5.0)
    comment: Optional[str] = None