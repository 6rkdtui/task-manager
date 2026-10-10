import pytest
import os
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from api import app
from database import get_connection


@pytest.fixture
def client():
    flag_loading = load_dotenv(".env.test", override=True)
    if flag_loading is False:
        raise RuntimeError("Не удалось загрузить '.env.test'")

    if os.getenv("DB_NAME") != "task_manager_test":
        raise RuntimeError("Тесты должны использовать базу task_manager_test")

    with TestClient(app) as client:
        test_connection = get_connection()
        try:
            with test_connection.cursor() as cursor:
                cursor.execute("DELETE FROM tasks")
            test_connection.commit()

            yield client

        finally:
            try:
                with test_connection.cursor() as cursor:
                    cursor.execute("DELETE FROM tasks")
                test_connection.commit()
            finally:
                test_connection.close()


def test_create_and_get_task(client):
    response_for_create = client.post(
        "/tasks",
        json={"title": "Купить продукты", "description": "Молоко и хлеб"},
    )
    assert response_for_create.status_code == 201

    created_id = response_for_create.json()["id"]

    response_for_get = client.get(f"/tasks/{created_id}")
    assert response_for_get.status_code == 200

    assert response_for_get.json()["id"] == created_id
    assert response_for_get.json()["title"] == response_for_create.json()["title"]
    assert (
        response_for_get.json()["description"]
        == response_for_create.json()["description"]
    )
    assert (
        response_for_get.json()["is_completed"]
        == response_for_create.json()["is_completed"]
    )
