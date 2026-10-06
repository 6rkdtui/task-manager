from fastapi import FastAPI, Depends, HTTPException

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


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, service: TaskService = Depends(get_service)):
    task = service.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    return task


@app.get("/tasks", response_model=list[TaskResponse])
def get_all_tasks(service: TaskService = Depends(get_service)):
    return service.get_all_tasks()
