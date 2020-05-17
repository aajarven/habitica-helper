"""
Test utility functions
"""

import datetime
import pytest

from freezegun import freeze_time

from habitica_helper import utils


@freeze_time("2020-05-05")
@pytest.mark.parametrize(
    ["weekday_str", "correct_date"],
    [
        ("mon", datetime.date(2020, 5, 11)),
        ("tue", datetime.date(2020, 5, 12)),
        ("wed", datetime.date(2020, 5, 6)),
        ("thu", datetime.date(2020, 5, 7)),
        ("fri", datetime.date(2020, 5, 8)),
        ("sat", datetime.date(2020, 5, 9)),
        ("sun", datetime.date(2020, 5, 10)),
        ("Thu", datetime.date(2020, 5, 7)),
        ("Thursday", datetime.date(2020, 5, 7)),
        ("THURSDAY", datetime.date(2020, 5, 7)),
    ]
)
def test_get_next_weekday(weekday_str, correct_date):
    """
    Test that get_next_weekday returns the correct date.
    """
    next_weekday_date = utils.get_next_weekday(weekday_str)
    assert next_weekday_date == correct_date


@freeze_time("2019-12-27")
@pytest.mark.parametrize(
    ["weekday_str", "correct_date"],
    [
        ("mon", datetime.date(2019, 12, 30)),
        ("wed", datetime.date(2020, 1, 1)),
        ("fri", datetime.date(2020, 1, 3)),
    ]
)
def test_get_next_weekday_over_newyear(weekday_str, correct_date):
    """
    Test that get_next_weekday is able to handle a new month/year.
    """
    next_weekday_date = utils.get_next_weekday(weekday_str)
    assert next_weekday_date == correct_date
