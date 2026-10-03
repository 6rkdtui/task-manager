from database import get_connection

if __name__ == "__main__":
    connection = get_connection()

    print("Подключение успешное")

    connection.close()
