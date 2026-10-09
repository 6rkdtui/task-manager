import pytest
from unittest.mock import Mock
from task import Task
from task_service import TaskService
from task_repository import TaskRepository


@pytest.fixture
def mock_repository():
    return Mock(spec=TaskRepository)


@pytest.fixture
def service(mock_repository):
    return TaskService(mock_repository)


def test_get_task(service, mock_repository):
    task = Task(
        id=1,
        title="test_title",
        description="test_desc",
        is_completed=False,
    )

    mock_repository.get_task.return_value = task
    result = service.get_task(1)
    assert result == task
    mock_repository.get_task.assert_called_once_with(1)


def test_add_task_title_only_spaces(service, mock_repository):
    with pytest.raises(ValueError):
        service.add_task("   ", "Описание")

    mock_repository.add_task.assert_not_called()


def test_add_task_description_only_spaces(service, mock_repository):
    with pytest.raises(ValueError):
        service.add_task("Названеи", "   ")

    mock_repository.add_task.assert_not_called()


def test_complete_task(service, mock_repository):
    task = Task(
        id=1,
        title="test_title",
        description="test_desc",
        is_completed=False,
    )

    completed_task = Task(
        id=1,
        title="test_title",
        description="test_desc",
        is_completed=True,
    )

    mock_repository.get_task.return_value = task
    mock_repository.complete_task.return_value = completed_task
    result = service.complete_task(1)
    assert result == completed_task
    mock_repository.get_task.assert_called_once_with(1)
    mock_repository.complete_task.assert_called_once_with(1)


def test_complete_task_already_completed(service, mock_repository):
    task = Task(
        id=1,
        title="test_title",
        description="test_desc",
        is_completed=True,
    )

    mock_repository.get_task.return_value = task
    result = service.complete_task(1)

    assert result == task
    mock_repository.get_task.assert_called_once_with(1)
    mock_repository.complete_task.assert_not_called()


def test_complete_task_not_found(service, mock_repository):
    mock_repository.get_task.return_value = None
    result = service.complete_task(1)

    assert result is None
    mock_repository.get_task.assert_called_once_with(1)
    mock_repository.complete_task.assert_not_called()


def test_delete_task(service, mock_repository):
    task = Task(
        id=1,
        title="test_title",
        description="test_desc",
        is_completed=False,
    )

    mock_repository.get_task.return_value = task

    result = service.delete_task(1)

    assert result == task
    mock_repository.get_task.assert_called_once_with(1)
    mock_repository.delete_task.assert_called_once_with(1)


def test_delete_task_not_found(service, mock_repository):
    mock_repository.get_task.return_value = None
    result = service.delete_task(1)

    assert result is None
    mock_repository.get_task.assert_called_once_with(1)
    mock_repository.delete_task.assert_not_called()


def test_update_task(service, mock_repository):
    task = Task(
        id=1,
        title="test_title",
        description="test_desc",
        is_completed=False,
    )

    updated_task = Task(
        id=1,
        title="test_updated_title",
        description="test_updated_desc",
        is_completed=False,
    )

    mock_repository.get_task.return_value = task
    mock_repository.update_task.return_value = updated_task
    result = service.update_task(
        1,
        "test_updated_title",
        "test_updated_desc",
    )

    assert result == updated_task
    mock_repository.get_task.assert_called_once_with(1)
    mock_repository.update_task.assert_called_once_with(
        1,
        "test_updated_title",
        "test_updated_desc",
    )


def test_update_task_not_found(service, mock_repository):
    mock_repository.get_task.return_value = None
    result = service.update_task(1)

    assert result is None
    mock_repository.get_task.assert_called_once_with(1)
    mock_repository.update_task.assert_not_called()


def test_update_task_title_only_spaces(service, mock_repository):
    mock_repository.get_task.return_value = Task(
        id=1,
        title="Старое название",
        description="Описание",
    )

    with pytest.raises(ValueError):
        service.update_task(1, "   ", None)

    mock_repository.update_task.assert_not_called()


def test_update_task_description_only_spaces(service, mock_repository):
    mock_repository.get_task.return_value = Task(
        id=1,
        title="Название",
        description="Старое описание",
    )

    with pytest.raises(ValueError):
        service.update_task(1, None, "   ")

    mock_repository.update_task.assert_not_called()


def test_add_task(service, mock_repository):
    task = Task(
        id=1,
        title="test_title",
        description="test_desc",
        is_completed=False,
    )

    mock_repository.add_task.return_value = task

    result = service.add_task("test_title", "test_desc")

    assert result == task
    mock_repository.add_task.assert_called_once_with(
        "test_title",
        "test_desc",
    )


def test_get_all_tasks(service, mock_repository):
    tasks = [
        Task(
            id=1,
            title="test_title_1",
            description="test_desc_1",
            is_completed=False,
        ),
        Task(
            id=2,
            title="test_title_2",
            description="test_desc_2",
            is_completed=False,
        ),
    ]

    mock_repository.get_all_tasks.return_value = tasks
    result = service.get_all_tasks()

    assert result == tasks
    mock_repository.get_all_tasks.assert_called_once()


def test_close(service, mock_repository):
    service.close()
    mock_repository.close.assert_called_once()
