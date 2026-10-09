from typing import Annotated
from pydantic import BaseModel, StringConstraints

NonBlankText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class TaskCreate(BaseModel):
    title: NonBlankText
    description: NonBlankText


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    is_completed: bool


class TaskUpdate(BaseModel):
    title: NonBlankText
    description: NonBlankText
