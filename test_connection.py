from database import get_connection

connection = get_connection()

print("Подключение успешное")

connection.close()
