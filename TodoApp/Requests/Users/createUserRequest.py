from typing import Optional

from pydantic import BaseModel, Field, field_validator

class CreateUserRequest(BaseModel):
    username: str = Field(description="The username")
    email: str = Field(description="The email address")
    password: str = Field(description="The user's password")
    first_name: str = Field(description="The first name")
    last_name: str = Field(description="The last name")
    roles: Optional[str] = Field(description="The roles of the user")
    is_active: Optional[bool] = Field(description="Whether the user is active", default=True)

    @field_validator('first_name')
    def first_name_validator(cls, v):
        assert 2 < len(v) <= 50

        return v

    @field_validator('last_name')
    def last_name_validator(cls, v):
        assert 2 < len(v) <= 50

        return v

    @field_validator('email')
    def email_validator(cls, v):
        assert 2 < len(v) <= 50

        return v
