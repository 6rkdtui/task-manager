from task_repository import TaskRepository
from task import Task


class TaskService:

    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository

    def get_task(self, task_id: int) -> Task | None:
        return self.repository.get_task(task_id)

    def get_all_tasks(self) -> list[Task]:
        return self.repository.get_all_tasks()

    def complete_task(self, task_id: int) -> Task | None:
        task = self.repository.get_task(task_id)

        if task is None:
            return None

        if task.is_completed:
            return task

        return self.repository.complete_task(task_id)

    def delete_task(self, task_id: int) -> Task | None:
        task = self.repository.get_task(task_id)

        if task is None:
            return None

        self.repository.delete_task(task_id)
        return task

    def update_task(
        self, task_id: int, title: str | None = None, description: str | None = None
    ) -> Task | None:
        task = self.repository.get_task(task_id)

        if task is None:
            return None

        if title is not None:
            title = title.strip()
            if not title:
                raise ValueError("Название задачи не может быть пустым")

        if description is not None:
            description = description.strip()
            if not description:
                raise ValueError("Описание задачи не может быть пустым")

        return self.repository.update_task(task_id, title, description)

    def add_task(self, title: str, description: str) -> Task:
        title = title.strip()
        description = description.strip()

        if not title:
            raise ValueError("Название задачи не может быть пустым")

        if not description:
            raise ValueError("Описание задачи не может быть пустым")

        return self.repository.add_task(title, description)

    def close(self) -> None:
        self.repository.close()
