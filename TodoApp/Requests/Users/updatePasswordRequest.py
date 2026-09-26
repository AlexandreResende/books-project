from pydantic import BaseModel, Field

class UpdatePasswordRequest(BaseModel):
    password: str = Field(description="The new password")