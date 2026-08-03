from typing import Optional

from pydantic import BaseModel, Field, field_validator

class UpdateBookRequest(BaseModel):
    author: Optional[str] = Field(description="Name of the author", default=None)
    title: Optional[str] = Field(description="Title of the book", default=None)
    description: Optional[str] = Field(description="A brief description of the book", default=None)
    rating: Optional[int] = Field(description="The new rating of the movie", default=None)
    published_year_date: Optional[int] = Field(description="The year the book was published", default=None)

    @field_validator("published_year_date")
    @classmethod
    def validate_published_year_date(cls, published_year_date):
        if published_year_date is not None:
            assert published_year_date > 1300

        return published_year_date

    @field_validator("author")
    @classmethod
    def validate_author(cls, author):
        if author is not None:
            assert len(author) < 100

        return author

    @field_validator("title")
    @classmethod
    def validate_title(cls, title):
        if title is not None:
            assert len(title) < 100

        return title

    @field_validator("description")
    @classmethod
    def validate_description(cls, description):
        if description is not None:
            assert len(description) < 150

        return description

    @field_validator("rating")
    @classmethod
    def validate_rating(cls, rating):
        if rating is not None:
            assert 0 < rating < 6

        return rating