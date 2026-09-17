from task_manager import TaskManager

manager = TaskManager()

while True:
    option_input = int(input("Выберите нужную опцию ..."))

    match option_input:
        case 0:
            break

        case 1:
            title = input("Введите назавание задачи ")
            description = input("Введите описание задачи ")
            task = manager.add_task(title, description)
            print(task)

        case 2:
            tasks = manager.get_all_tasks()
            if not tasks:
                print("Задач пока нет")
            else:
                for task in tasks:
                    print(task)


# if __name__ == "__main__":
#     manager = TaskManager()
#     task1 = manager.add_task("Изучить ООП", "Закончить курс по ООП")
#     task2 = manager.add_task("Изучить Docker", "Пройти базовый курс")

#     print("После добавления:")
#     print(manager.get_all_tasks())

#     print("\nПолучение задачи с id=1:")
#     print(manager.get_task(1))

#     print("\nНесуществующая задача:")
#     print(manager.get_task(100))

#     print("\nПосле изменения:")
#     manager.update_task(1, title="Повторить ООП")
#     print(manager.get_task(1))

#     print("\nПосле complete_task:")
#     manager.complete_task(1)
#     print(manager.get_task(1))

#     print("\nУдаляем задачу 2:")
#     deleted_task = manager.delete_task(2)
#     print("Удалена:", deleted_task)
#     print(manager.get_all_tasks())
