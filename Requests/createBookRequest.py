from typing import Optional

from pydantic import BaseModel, Field, ValidationError, field_validator

class CreateBookRequest(BaseModel):
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    description: Optional[str] = None
    rating: int = Field(gt=0, lt=6)

    @field_validator('description')
    @classmethod
    def validate_description(cls, description):
        if description is not None:
            assert len(description) < 150
            return description

        return None