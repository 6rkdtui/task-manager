from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    description: str


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    is_completed: bool
