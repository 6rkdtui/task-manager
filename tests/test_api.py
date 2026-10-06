from fastapi.testclient import TestClient
from unittest.mock import Mock

from api import app, get_service
from task_service import TaskService
from task import Task


def test_create_task():
    fake_service = Mock(spec=TaskService)

    fake_service.add_task.return_value = Task(
        id=1,
        title="Купить продукты",
        description="Молоко и хлеб",
    )

    app.dependency_overrides[get_service] = lambda: fake_service

    try:
        client = TestClient(app)

        response = client.post(
            "/tasks",
            json={"title": "Купить продукты", "description": "Молоко и хлеб"},
        )

        assert response.status_code == 201
        assert response.json() == {
            "id": 1,
            "title": "Купить продукты",
            "description": "Молоко и хлеб",
            "is_completed": False,
        }
        fake_service.add_task.assert_called_once_with(
            "Купить продукты", "Молоко и хлеб"
        )

    finally:
        app.dependency_overrides.pop(get_service, None)


def test_create_task_without_title():
    fake_service = Mock(spec=TaskService)

    app.dependency_overrides[get_service] = lambda: fake_service

    try:
        client = TestClient(app)

        response = client.post(
            "/tasks",
            json={"description": "Молоко и хлеб"},
        )

        assert response.status_code == 422
        assert response.json()["detail"][0]["loc"] == ["body", "title"]
        fake_service.add_task.assert_not_called()

    finally:
        app.dependency_overrides.pop(get_service, None)


def test_get_task():
    fake_service = Mock(spec=TaskService)

    fake_service.get_task.return_value = Task(
        id=1, title="Купить продукты", description="Молоко и хлеб", is_completed=True
    )

    app.dependency_overrides[get_service] = lambda: fake_service

    try:
        client = TestClient(app)

        response = client.get("/tasks/1")

        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "title": "Купить продукты",
            "description": "Молоко и хлеб",
            "is_completed": True,
        }
        fake_service.get_task.assert_called_once_with(1)

    finally:
        app.dependency_overrides.pop(get_service, None)


def test_get_task_not_found():
    fake_service = Mock(spec=TaskService)

    fake_service.get_task.return_value = None

    app.dependency_overrides[get_service] = lambda: fake_service

    try:
        client = TestClient(app)

        response = client.get("/tasks/1")

        assert response.status_code == 404
        assert response.json() == {"detail": "Задача не найдена"}
        fake_service.get_task.assert_called_once_with(1)

    finally:
        app.dependency_overrides.pop(get_service, None)


def test_get_all_tasks():
    fake_service = Mock(spec=TaskService)

    fake_service.get_all_tasks.return_value = [
        Task(
            id=1,
            title="Купить продукты",
            description="Молоко и хлеб",
            is_completed=True,
        ),
        Task(
            id=2,
            title="Убраться дома",
            description="Пропылесосить и помыть полы",
            is_completed=False,
        ),
    ]

    app.dependency_overrides[get_service] = lambda: fake_service

    try:
        client = TestClient(app)

        response = client.get("/tasks")

        assert response.status_code == 200
        assert response.json() == [
            {
                "id": 1,
                "title": "Купить продукты",
                "description": "Молоко и хлеб",
                "is_completed": True,
            },
            {
                "id": 2,
                "title": "Убраться дома",
                "description": "Пропылесосить и помыть полы",
                "is_completed": False,
            },
        ]
        fake_service.get_all_tasks.assert_called_once_with()

    finally:
        app.dependency_overrides.pop(get_service, None)


def test_get_all_tasks_without_tasks():
    fake_service = Mock(spec=TaskService)

    fake_service.get_all_tasks.return_value = []

    app.dependency_overrides[get_service] = lambda: fake_service

    try:
        client = TestClient(app)

        response = client.get("/tasks")

        assert response.status_code == 200
        assert response.json() == []
        fake_service.get_all_tasks.assert_called_once_with()

    finally:
        app.dependency_overrides.pop(get_service, None)


def test_update_task():
    fake_service = Mock(spec=TaskService)

    fake_service.update_task.return_value = Task(
        id=1,
        title="Купить продукты",
        description="Молоко и хлеб",
        is_completed=False,
    )

    app.dependency_overrides[get_service] = lambda: fake_service

    try:
        client = TestClient(app)

        response = client.put(
            "/tasks/1",
            json={
                "title": "Купить продукты",
                "description": "Молоко и хлеб",
            },
        )

        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "title": "Купить продукты",
            "description": "Молоко и хлеб",
            "is_completed": False,
        }
        fake_service.update_task.assert_called_once_with(
            1, "Купить продукты", "Молоко и хлеб"
        )

    finally:
        app.dependency_overrides.pop(get_service, None)


def test_update_task_not_found():
    fake_service = Mock(spec=TaskService)

    fake_service.update_task.return_value = None

    app.dependency_overrides[get_service] = lambda: fake_service

    try:
        client = TestClient(app)

        response = client.put(
            "/tasks/1",
            json={
                "title": "Купить продукты",
                "description": "Молоко и хлеб",
            },
        )

        assert response.status_code == 404
        assert response.json() == {"detail": "Задача не найдена"}
        fake_service.update_task.assert_called_once_with(
            1, "Купить продукты", "Молоко и хлеб"
        )

    finally:
        app.dependency_overrides.pop(get_service, None)


def test_update_task_without_description():
    fake_service = Mock(spec=TaskService)

    app.dependency_overrides[get_service] = lambda: fake_service

    try:
        client = TestClient(app)

        response = client.put(
            "/tasks/1",
            json={
                "title": "Купить продукты",
            },
        )

        assert response.status_code == 422
        assert response.json()["detail"][0]["loc"] == ["body", "description"]
        fake_service.update_task.assert_not_called()

    finally:
        app.dependency_overrides.pop(get_service, None)


def test_complete_task():
    fake_service = Mock(spec=TaskService)

    fake_service.complete_task.return_value = Task(
        id=1,
        title="Купить продукты",
        description="Молоко и хлеб",
        is_completed=True,
    )

    app.dependency_overrides[get_service] = lambda: fake_service

    try:
        client = TestClient(app)

        response = client.patch(
            "/tasks/1/complete",
        )

        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "title": "Купить продукты",
            "description": "Молоко и хлеб",
            "is_completed": True,
        }
        fake_service.complete_task.assert_called_once_with(1)

    finally:
        app.dependency_overrides.pop(get_service, None)


def test_complete_task_not_found():
    fake_service = Mock(spec=TaskService)

    fake_service.complete_task.return_value = None

    app.dependency_overrides[get_service] = lambda: fake_service

    try:
        client = TestClient(app)

        response = client.patch(
            "/tasks/1/complete",
        )

        assert response.status_code == 404
        assert response.json() == {"detail": "Задача не найдена"}
        fake_service.complete_task.assert_called_once_with(1)

    finally:
        app.dependency_overrides.pop(get_service, None)


def test_delete_task():
    fake_service = Mock(spec=TaskService)

    fake_service.delete_task.return_value = Task(
        id=1,
        title="Купить продукты",
        description="Молоко и хлеб",
        is_completed=True,
    )

    app.dependency_overrides[get_service] = lambda: fake_service

    try:
        client = TestClient(app)

        response = client.delete(
            "/tasks/1",
        )

        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "title": "Купить продукты",
            "description": "Молоко и хлеб",
            "is_completed": True,
        }
        fake_service.delete_task.assert_called_once_with(1)

    finally:
        app.dependency_overrides.pop(get_service, None)


def test_delete_task_not_found():
    fake_service = Mock(spec=TaskService)

    fake_service.delete_task.return_value = None

    app.dependency_overrides[get_service] = lambda: fake_service

    try:
        client = TestClient(app)

        response = client.delete(
            "/tasks/1",
        )

        assert response.status_code == 404
        assert response.json() == {"detail": "Задача не найдена"}
        fake_service.delete_task.assert_called_once_with(1)

    finally:
        app.dependency_overrides.pop(get_service, None)
