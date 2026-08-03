from typing import Optional

from pydantic import BaseModel, Field, ValidationError, field_validator

class CreateBookRequest(BaseModel):
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    description: Optional[str] = Field(default=None, description="Description field is optional, but if present must have less than 150 characters")
    rating: int = Field(gt=0, lt=6)
    published_year_date: Optional[int] = Field(default=None, description="The year the book was published")

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Fluent Python",
                "author": "Luciano Ramalho",
                "description": "Python book from zero to hero",
                "rating": 5,
                "published_year_date": 2010
            }
        }
    }

    @field_validator("description")
    @classmethod
    def validate_description(cls, description):
        if description is not None:
            assert len(description) < 150
            return description

        return None

    @field_validator("published_year_date")
    @classmethod
    def validate_published_year_date(cls, published_year_date):
        if published_year_date is not None:
            assert published_year_date > 1300

        return published_year_date