from fastapi import FastAPI, Depends, HTTPException

from task_repository import TaskRepository
from task_service import TaskService
from schemas import TaskCreate, TaskResponse, TaskUpdate

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


@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int, task: TaskUpdate, service: TaskService = Depends(get_service)
):
    updated_task = service.update_task(task_id, task.title, task.description)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    return updated_task


@app.patch("/tasks/{task_id}/complete", response_model=TaskResponse)
def complete_task(task_id: int, service: TaskService = Depends(get_service)):
    completed_task = service.complete_task(task_id)
    if completed_task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    return completed_task


@app.delete("/tasks/{task_id}", response_model=TaskResponse)
def delete_task(task_id: int, service: TaskService = Depends(get_service)):
    deleted_task = service.delete_task(task_id)
    if deleted_task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    return deleted_task
