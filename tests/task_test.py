"""
Test that the input data validation works when creating a Task.
"""

import pytest

from habitica_helper.task import Task


DEFAULTS = {
    "notes": "",
    "date": None,
    "difficulty": 1,
    "uppable": "true",
    "downable": "false",
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
        "difficulty": 2,
    }
    task = Task(taskdata)
    for key in taskdata:
        assert getattr(task, key) == taskdata[key]


@pytest.mark.parametrize(
    ["attr", "value"],
    [
        ("text", ""),
        ("text", None),
        ("text", ["task name"]),
        ("notes", ["task notes"]),
        ("date", "not a valid date"),
        ("date", ["no not a", "valid date"]),
        ("frequency", "every minute"),
        ("uppable", "totally"),
        ("downable", "hell yeah"),
    ]
)
def test_illegal_values(attr, value):
    """
    Test that illegal values raise an exception
    """
    task_data = {"text": "test task",
                 "tasktype": "todo",
                 "notes": "some notes for this task",
                 }
    task_data[attr] = value
    with pytest.raises(ValueError):
        Task(task_data)


def test_equals():
    """
    Test that tasks are compared on tasktype, text and notes for equality.
    """
    base_data = {"text": "test task",
                 "tasktype": "todo",
                 "notes": "some notes for this task",
                 "difficulty": "easy"}
    task = Task(base_data)

    # task equals itself
    assert task == task  # pylint: disable=comparison-with-itself

    # task doesn't equal a dict with the same data
    assert task != base_data

    # tasks with equal properties equal
    task2 = Task(base_data)
    assert task == task2

    # tasks with equal type, text and notes equal
    task2.difficulty = "hard"
    assert task == task2

    # tasks with different type, text or notes aren't equal
    for attr, value in [("text", "different text"),
                        ("tasktype", "habit"),
                        ("notes", "different notes"),
                        ]:
        different_data = dict(base_data)
        different_data[attr] = value
        task2 = Task(different_data)
        assert task != task2
