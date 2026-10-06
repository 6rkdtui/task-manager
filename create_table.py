from database import get_connection


def create_tasks_table(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            is_completed BOOLEAN NOT NULL DEFAULT FALSE
            );
        """)

        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()


if __name__ == "__main__":
    connection = get_connection()
    try:
        create_tasks_table(connection)
    finally:
        connection.close()
