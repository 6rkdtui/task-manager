from task import Task
import sqlite3


class TaskManager:
    def __init__(self, db_name: str) -> None:
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)

    def add_task(self, title: str, description: str) -> Task:
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO tasks (title, description) VALUES (?, ?)", (title, description)
        )
        self.connection.commit()

        new_id = cursor.lastrowid
        task = Task(new_id, title, description)

        cursor.close()
        return task

    def get_task(self, task_id: int) -> Task | None:
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT id, title, description, is_completed FROM tasks WHERE id = ?",
            (task_id,),
        )
        task = cursor.fetchone()
        cursor.close()
        if task is None:
            return None

        return Task(task[0], task[1], task[2], bool(task[3]))

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
