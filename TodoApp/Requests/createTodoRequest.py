from typing import Optional

from pydantic import BaseModel, Field, field_validator

class CreateTodoRequest(BaseModel):
    title: str = Field(description="The title of the todo to be achieved")
    description: Optional[str] = Field(description="The description of the todo to be achieved")
    priority: int = Field(description="The priority relevante of the todo. From 1 to 5 where 1 is the highest priority")
    completed: Optional[bool] = Field(description="The status of the todo. If not passed the default value is False", default=False)

    @field_validator("title")
    @classmethod
    def validate_title(cls, title):
        assert 3 < len(title) < 100

        return title

    @field_validator("description")
    @classmethod
    def validate_description(cls, description):
        if description is not None:
            assert 5 < len(description) < 150

        return description

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, priority):
        assert 1 <= priority <= 5

        return priority

    @field_validator("completed")
    @classmethod
    def validate_completed(cls, completed):
        if completed is not None:
            assert completed == True or completed == False

        return completed