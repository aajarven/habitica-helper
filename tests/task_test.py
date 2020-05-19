"""
Test that the input data validation works when creating a Task.
"""

import pytest

from habitica_helper.task import Task


DEFAULTS = {
    "notes": "",
    "date": None,
    "difficulty": "easy",
    "uppable": True,
    "downable": False,
}


def test_create_minimal_task():
    """
    Test that creating a task with a minimal set of attributes works.
    """
    task = Task({"text": "test task", "tasktype": "daily"})
    assert task.text == "test task"
    assert task.tasktype == "daily"
    for key in DEFAULTS:
        assert getattr(task, key) == DEFAULTS[key]


@pytest.mark.parametrize(
    "taskdata",
    [
        {"text": "test task"},
        {"tasktype": "daily"},
        {"text": "test task", "tasktype": "not_supported"},
        {"text": "test task", "tasktype": "daily", "date": "notadate"},
        {"text": "test task", "tasktype": "daily", "difficulty": "notdiff"},
        {"text": "test task", "tasktype": "daily", "uppable": "not a bool"},
    ]
)
def test_create_bad_task(taskdata):
    """
    Test that a ValueError is raised when illegal values are provided.
    """
    with pytest.raises(ValueError):
        Task(taskdata)


def test_create_difficult_task():
    """
    Test complicated task creation
    """
    taskdata = {
        "text": ("a long long task name, I mean this is going to take some "
                 "space. Oh, and did I mention it is going to have some "
                 "difficult characters too? Dämń, Ï müŝt have förgötten."),
        "tasktype": "todo",
        "notes": "Not much to say here. 🙊",
        "date": "2020-05-19",
        "difficulty": "hard",
    }
    task = Task(taskdata)
    for key in taskdata:
        assert getattr(task, key) == taskdata[key]
