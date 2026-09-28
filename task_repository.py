from database import get_connection
from task import Task


class TaskRepository:

    def __init__(self) -> None:
        self.connection = get_connection()
        self._create_table()

    def _create_table(self) -> None:
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY, 
                    title TEXT NOT NULL, 
                    description TEXT, 
                    is_completed BOOLEAN NOT NULL DEFAULT FALSE
                ) 
                """)

            self.connection.commit()
        except Exception:
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
                "SELECT id, title, description, is_completed FROM tasks WHERE id = %s",
                (task_id,),
            )
            row = cursor.fetchone()
        finally:
            cursor.close()

        if row is None:
            return None

        return Task(row[0], row[1], row[2], row[3])

    def add_task(self, title: str, description: str) -> Task:
        cursor = self.connection.cursor()

        try:
            cursor.execute(
                "INSERT INTO tasks (title, description) VALUES (%s, %s) RETURNING id",
                (title, description),
            )
            row = cursor.fetchone()

            if row is None:
                raise RuntimeError("Не удалось получить ID новой задачи")

            self.connection.commit()

            return Task(row[0], title, description)
        except Exception:
            self.connection.rollback()
            raise
        finally:
            cursor.close()

    def get_all_tasks(self) -> list[Task]:
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "SELECT id, title, description, is_completed FROM tasks ORDER BY id"
            )
            rows = [Task(row[0], row[1], row[2], row[3]) for row in cursor.fetchall()]
        finally:
            cursor.close()

        return rows

    def complete_task(self, task_id: int) -> Task | None:
        task = self.get_task(task_id)

        if task is None:
            return None

        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "UPDATE tasks SET is_completed = TRUE WHERE id = %s",
                (task_id,),
            )
            self.connection.commit()
        except Exception:
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
            cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
            self.connection.commit()
        except Exception:
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
                    "UPDATE tasks SET title = %s WHERE id = %s", (title, task_id)
                )

            if description is not None:
                cursor.execute(
                    "UPDATE tasks SET description = %s WHERE id = %s",
                    (description, task_id),
                )

            self.connection.commit()
        except Exception:
            self.connection.rollback()
            raise
        finally:
            cursor.close()

        if title is not None:
            task.title = title

        if description is not None:
            task.description = description

        return task
