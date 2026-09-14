from dataclasses import dataclass


@dataclass
class Task:
    id: int
    title: str
    description: str
    is_completed: bool = False


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


if __name__ == "__main__":
    manager = TaskManager()
    task1 = manager.add_task("Изучить ООП", "Закончить курс по ООП")
    task2 = manager.add_task("Изучить Docker", "Пройти базовый курс")

    print("После добавления:")
    print(manager.get_all_tasks())

    print("\nПолучение задачи с id=1:")
    print(manager.get_task(1))

    print("\nНесуществующая задача:")
    print(manager.get_task(100))

    print("\nПосле изменения:")
    manager.update_task(1, title="Повторить ООП")
    print(manager.get_task(1))

    print("\nПосле complete_task:")
    manager.complete_task(1)
    print(manager.get_task(1))

    print("\nУдаляем задачу 2:")
    deleted_task = manager.delete_task(2)
    print("Удалена:", deleted_task)
    print(manager.get_all_tasks())
