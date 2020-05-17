"""
Miscellaneous small utility functions.
"""

import datetime
import requests


def get_dict_from_api(header, url):
    """
    Get data dict for API call represented by the given url.

    :header: HTTP header required when making Habitica API calls
    :url: URL for API get request
    :returns: Dict containing the data

    :raises: HTTPError if the request was bad
    """
    response = requests.get(url, headers=header)
    response.raise_for_status()
    return response.json()["data"]


def get_next_weekday(weekday):
    """
    Return a datetime object representing the next time it's the given day.

    :weekday: Name of the weekday. Allowed values are e.g. "Tuesday",
              "tuesday", "Tue" and "tue".
    :returns: date object
    """
    day_numbers = {
        "mon": 0,
        "tue": 1,
        "wed": 2,
        "thu": 3,
        "fri": 4,
        "sat": 5,
        "sun": 6
        }
    today = datetime.date.today()
    try:
        goal_day_number = day_numbers[weekday[:3].lower()]
    except KeyError:
        raise KeyError("Weekday {} not recognized".format(weekday))
    today_day_number = today.weekday()

    next_day = (today +
                datetime.timedelta((goal_day_number - today_day_number) % 7))
    if next_day == today:
        next_day = next_day + datetime.timedelta(7)

    return next_day
