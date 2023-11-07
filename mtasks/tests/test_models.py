import pytest

from django.core.exceptions import ValidationError

from mtasks.models import Task, State, Priority


pytestmark = pytest.mark.django_db(transaction=True)


@pytest.fixture()
def task1() -> Task:
    task = Task(title='The title')
    task.save()
    return task


def test_automated_default_fields(task1: Task):
    assert task1.pk is not None
    assert task1.number == '00000001'
    assert task1.state == State.TO_DO.value
    assert task1.priority == Priority.NORMAL.value


def test_validate_title(task1: Task):
    # Create a second task with the same task fails
    task2 = Task(title='The title 1')
    task2.clean()   # No exception
    task2.title = 'The title'
    with pytest.raises(ValidationError):
        task2.clean()
