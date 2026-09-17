from task import Task


class TaskManager:
    def __init__(self) -> None:
        self.tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def add_task(self, title: str, description: str) -> Task:
        task = Task(self._next_id, title, description)
        self.tasks[self._next_id] = task
        self._next_id += 1
        return task

    def get_task(self, task_id: int) -> Task | None:
        if task_id in self.tasks:
            return self.tasks[task_id]

        return None

    def get_all_tasks(self) -> list[Task]:
        return list(self.tasks.values())

    def complete_task(self, task_id: int) -> Task | None:
        task = self.get_task(task_id)
        if task is None:
            return None

        task.is_completed = True
        return task

    def delete_task(self, task_id: int) -> Task | None:
        task = self.get_task(task_id)
        if task is None:
            return None

        del self.tasks[task_id]
        return task

    def update_task(
        self, task_id: int, title: str | None = None, description: str | None = None
    ) -> Task | None:
        task = self.get_task(task_id)

        if task is None:
            return None

        if title is not None:
            task.title = title

        if description is not None:
            task.description = description

        return task
