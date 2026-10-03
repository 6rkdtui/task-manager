from fastapi import FastAPI, Depends

from task_repository import TaskRepository
from task_service import TaskService
from schemas import TaskCreate, TaskResponse

app = FastAPI()


def get_service():
    repository = TaskRepository()
    service = TaskService(repository)

    try:
        yield service
    finally:
        service.close()


@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate, service: TaskService = Depends(get_service)):
    added_task = service.add_task(task.title, task.description)
    return added_task
