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
