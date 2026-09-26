import pytest
from task_repository import TaskRepository


@pytest.fixture
def repository(tmp_path):
    db_path = tmp_path / "test_task_manager.db"

    repo = TaskRepository(str(db_path))

    yield repo

    repo.close()


def test_add_task(repository):
    task = repository.add_task("test_title", "test_desc")

    assert task.title == "test_title"
    assert task.description == "test_desc"
    assert task.id is not None
    assert task.is_completed is False


def test_get_task(repository):
    created_task = repository.add_task("test_title", "test_desc")

    task = repository.get_task(created_task.id)

    assert task is not None
    assert task.id == created_task.id
    assert task.title == "test_title"
    assert task.description == "test_desc"
    assert task.is_completed is False


def test_get_all_tasks(repository):
    repository.add_task("test_title_1", "test_desc_1")
    repository.add_task("test_title_2", "test_desc_2")
    repository.add_task("test_title_3", "test_desc_3")

    tasks = repository.get_all_tasks()

    assert isinstance(tasks, list)
    assert len(tasks) == 3

    assert tasks[0].title == "test_title_1"
    assert tasks[1].title == "test_title_2"
    assert tasks[2].title == "test_title_3"

    assert tasks[0].description == "test_desc_1"
    assert tasks[1].description == "test_desc_2"
    assert tasks[2].description == "test_desc_3"

    assert tasks[0].is_completed is False
    assert tasks[1].is_completed is False
    assert tasks[2].is_completed is False


def test_complete_task(repository):
    created_task = repository.add_task("test_title", "test_desc")
    assert created_task.is_completed is False

    completed_task = repository.complete_task(created_task.id)
    assert completed_task is not None
    assert completed_task.is_completed is True

    task_from_db = repository.get_task(completed_task.id)
    assert task_from_db is not None
    assert task_from_db.is_completed is True


def test_update_task(repository):
    created_task_1 = repository.add_task("test_title", "test_desc")
    updated_task_1 = repository.update_task(
        created_task_1.id, "title_new_1", "desc_new_1"
    )

    assert updated_task_1 is not None
    assert updated_task_1.title == "title_new_1"
    assert updated_task_1.description == "desc_new_1"

    task_from_db = repository.get_task(created_task_1.id)
    assert task_from_db is not None
    assert task_from_db.title == "title_new_1"
    assert task_from_db.description == "desc_new_1"


def test_update_task_only_title(repository):
    created_task_2 = repository.add_task("test_title", "test_desc")
    updated_task_2 = repository.update_task(created_task_2.id, "title_new_2", None)

    assert updated_task_2 is not None
    assert updated_task_2.title == "title_new_2"
    assert updated_task_2.description == "test_desc"

    task_from_db = repository.get_task(created_task_2.id)
    assert task_from_db is not None
    assert task_from_db.title == "title_new_2"
    assert task_from_db.description == "test_desc"


def test_update_task_only_description(repository):
    created_task_3 = repository.add_task("test_title", "test_desc")
    updated_task_3 = repository.update_task(created_task_3.id, None, "desc_new_3")

    assert updated_task_3 is not None
    assert updated_task_3.title == "test_title"
    assert updated_task_3.description == "desc_new_3"

    task_from_db = repository.get_task(created_task_3.id)
    assert task_from_db is not None
    assert task_from_db.title == "test_title"
    assert task_from_db.description == "desc_new_3"


def test_update_task_no_changes(repository):
    created_task_4 = repository.add_task("test_title", "test_desc")
    updated_task_4 = repository.update_task(created_task_4.id, None, None)

    assert updated_task_4 is not None
    assert updated_task_4.id == created_task_4.id
    assert updated_task_4.title == created_task_4.title
    assert updated_task_4.description == created_task_4.description

    task_from_db = repository.get_task(created_task_4.id)
    assert task_from_db is not None
    assert task_from_db.title == "test_title"
    assert task_from_db.description == "test_desc"


def test_delete_task(repository):
    created_task = repository.add_task("test_title", "test_desc")
    deleted_task = repository.delete_task(created_task.id)

    assert deleted_task is not None
    assert deleted_task.id == created_task.id
    assert deleted_task.title == "test_title"
    assert deleted_task.description == "test_desc"
    assert deleted_task.is_completed is False

    task_from_db = repository.get_task(deleted_task.id)
    assert task_from_db is None


def test_get_task_not_found(repository):
    task = repository.get_task(999)

    assert task is None


def test_complete_task_not_found(repository):
    task = repository.complete_task(999)

    assert task is None


def test_update_task_not_found(repository):
    task = repository.update_task(999, "test_title", "test_desc")

    assert task is None


def test_delete_task_not_found(repository):
    task = repository.delete_task(999)

    assert task is None


def test_get_all_tasks_empty(repository):
    tasks = repository.get_all_tasks()

    assert tasks == []
