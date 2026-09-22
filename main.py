from task_repository import TaskRepository
from task_service import TaskService


def get_id() -> int:
    while True:
        try:
            task_id = int(input("Введите номер задачи: "))
            return task_id
        except ValueError:
            print("Вы ввели не число")


if __name__ == "__main__":
    repository = TaskRepository("task_manager.db")
    service = TaskService(repository)

    while True:
        print("""
            Выберите действие:

            1 — Добавить задачу
            2 — Показать все задачи
            3 — Показать задачу по ID
            4 — Изменить задачу
            5 — Отметить задачу выполненной
            6 — Удалить задачу
            0 — Выйти
        """)

        try:
            option_input = int(input("Выберите нужную опцию: "))
        except ValueError:
            print("Нужно ввести число")
            continue

        match option_input:
            case 0:
                service.close()
                break

            case 1:
                title = input("Введите название задачи: ")
                description = input("Введите описание задачи: ")
                task = service.add_task(title, description)
                print(task)

            case 2:
                tasks = service.get_all_tasks()
                if not tasks:
                    print("Задач пока нет")
                else:
                    for task in tasks:
                        print(task)

            case 3:
                task_id = get_id()

                task = service.get_task(task_id)
                if task is None:
                    print("Задача под данным номером отсутствует")
                else:
                    print(task)

            case 4:
                task_id = get_id()
                existing_task = service.get_task(task_id)
                if existing_task is None:
                    print("Задача под данным номером отсутствует")
                else:
                    new_title = input(
                        "Введите новое название или нажмите Enter, чтобы оставить без изменений: "
                    )
                    new_title = None if new_title == "" else new_title

                    new_description = input(
                        "Введите новое описание или нажмите Enter, чтобы оставить без изменений: "
                    )
                    new_description = None if new_description == "" else new_description

                    updated_task = service.update_task(
                        task_id, new_title, new_description
                    )

                    print(updated_task)

            case 5:
                task_id = get_id()
                completed_task = service.complete_task(task_id)
                if completed_task is None:
                    print("Задача под данным номером отсутствует")
                else:
                    print(completed_task)

            case 6:
                task_id = get_id()
                deleted_task = service.delete_task(task_id)
                if deleted_task is None:
                    print("Задача под данным номером отсутствует")
                else:
                    print(f"Задача удалена: {deleted_task}")

            case _:
                print("Такая команда отсутствует")
