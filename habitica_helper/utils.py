"""
Miscellaneous small utility functions.
"""

import datetime

from habitica_helper import habrequest


def get_dict_from_api(header, url):
    """
    Get data dict for API call represented by the given url.

    :header: HTTP header required when making Habitica API calls
    :url: URL for API get request
    :returns: Dict containing the data

    :raises: HTTPError if the request was bad
    """
    response = habrequest.get(url, headers=header)
    return response.json()["data"]


def get_next_weekday(weekday, from_date=None):
    """
    Return a date object representing the next time it's the given day.

    :weekday: Name of the weekday. Allowed values are e.g. "Tuesday",
              "tuesday", "Tue" and "tue".
    :from_date: Date from which the "next" is viewed. Defaults to the current
                date.
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
    try:
        goal_day_number = day_numbers[weekday[:3].lower()]
    except KeyError:
        raise KeyError("Weekday {} not recognized".format(weekday))
    if not from_date:
        from_date = datetime.date.today()
    start_day_number = from_date.weekday()

    next_day = (from_date +
                datetime.timedelta((goal_day_number - start_day_number) % 7))
    if next_day == from_date:
        next_day = next_day + datetime.timedelta(7)

    return next_day


def timestamp_to_datetime(timestamp_str):
    """
    Create a datetime object from a timestamp.

    The timestamp must be a string in habitica format, e.g.
    "2020-06-17T21:05:50.754Z".

    :returns: corresponding datetime
    """
    return datetime.datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ")
