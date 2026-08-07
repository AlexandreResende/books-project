from typing import Optional

from pydantic import Field, field_validator, BaseModel

class UpdateTodoRequest(BaseModel):
    title: Optional[str] = Field(description="Title of the task", default=None)
    description: Optional[str] = Field(description="description of the task", default=None)
    priority: Optional[int] = Field(description="Priority of the task from 1 to 5", default=None)
    completed: Optional[bool] = Field(description="If the task was already completed or not", default=None)

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