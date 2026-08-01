from typing import Optional

from pydantic import BaseModel, Field, ValidationError, field_validator

class CreateBookRequest(BaseModel):
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    description: Optional[str] = Field(default=None, description="Description field is optional, but if present must have less than 150 characters")
    rating: int = Field(gt=0, lt=6)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Fluent Python",
                "author": "Luciano Ramalho",
                "description": "Python book from zero to hero",
                "rating": 5
            }
        }
    }

    @field_validator('description')
    @classmethod
    def validate_description(cls, description):
        if description is not None:
            assert len(description) < 150
            return description

        return None