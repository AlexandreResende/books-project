from pydantic import BaseModel, Field, field_validator

class LoginRequest(BaseModel):
    username: str = Field(description="The username")
    password: str = Field(description="The password")

    @field_validator('username')
    def validate_username(cls, v):
        assert v.isalpha() and len(v) > 0

        return v

    @field_validator('password')
    def validate_password(cls, v):
        assert v.isalpha() and len(v) > 0

        return v