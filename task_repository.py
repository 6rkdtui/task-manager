import sqlite3
from task import Task


class TaskRepository:

    def __init__(self, db_name: str) -> None:
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self._create_table()

    def _create_table(self) -> None:
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title TEXT NOT NULL, 
                    description TEXT, 
                    is_completed BOOLEAN NOT NULL DEFAULT 0
                ) 
                """)

            self.connection.commit()
        except sqlite3.Error:
            self.connection.rollback()
            raise
        finally:
            cursor.close()

    def close(self) -> None:
        self.connection.close()

    def get_task(self, task_id: int) -> Task | None:
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "SELECT id, title, description, is_completed FROM tasks WHERE id = ?",
                (task_id,),
            )
            task = cursor.fetchone()
        finally:
            cursor.close()

        if task is None:
            return None

        return Task(task[0], task[1], task[2], bool(task[3]))

    def add_task(self, title: str, description: str) -> Task:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                "INSERT INTO tasks (title, description) VALUES (?, ?)",
                (title, description),
            )

            new_id = cursor.lastrowid
            if new_id is None:
                raise RuntimeError("Не удалось получить ID новой задачи")

            self.connection.commit()

            return Task(new_id, title, description)
        except sqlite3.Error:
            self.connection.rollback()
            raise
        finally:
            cursor.close()

    def get_all_tasks(self) -> list[Task]:
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT id, title, description, is_completed FROM tasks")
            tasks = [
                Task(task[0], task[1], task[2], bool(task[3]))
                for task in cursor.fetchall()
            ]
        finally:
            cursor.close()

        return tasks

    def complete_task(self, task_id: int) -> Task | None:
        task = self.get_task(task_id)

        if task is None:
            return None

        cursor = self.connection.cursor()
        try:
            cursor.execute("UPDATE tasks SET is_completed = 1 WHERE id = ?", (task_id,))
            self.connection.commit()
        except sqlite3.Error:
            self.connection.rollback()
            raise
        finally:
            cursor.close()

        task.is_completed = True
        return task

    def delete_task(self, task_id: int) -> Task | None:
        task = self.get_task(task_id)
        if task is None:
            return None

        cursor = self.connection.cursor()
        try:
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            self.connection.commit()
        except sqlite3.Error:
            self.connection.rollback()
            raise
        finally:
            cursor.close()

        return task

    def update_task(
        self, task_id: int, title: str | None = None, description: str | None = None
    ) -> Task | None:
        task = self.get_task(task_id)

        if task is None:
            return None

        cursor = self.connection.cursor()
        try:
            if title is not None:
                cursor.execute(
                    "UPDATE tasks SET title = ? WHERE id = ?", (title, task_id)
                )

            if description is not None:
                cursor.execute(
                    "UPDATE tasks SET description = ? WHERE id = ?",
                    (description, task_id),
                )

            self.connection.commit()
        except sqlite3.Error:
            self.connection.rollback()
            raise
        finally:
            cursor.close()

        if title is not None:
            task.title = title

        if description is not None:
            task.description = description

        return task
