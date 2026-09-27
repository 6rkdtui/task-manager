from database import get_connection

connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    is_completed BOOLEAN NOT NULL DEFAULT FALSE
    );
""")

connection.commit()
cursor.close()
connection.close()
