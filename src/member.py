"""
A class for representing Habitica user data.
"""

from datetime import datetime

from src import utils

class Member(object):
    """
    Habitica user.

    Has the following attributes:
    id                  User ID
    displayname         Nickname shown to others
    login_name          Player handle used for logging in
    habitica_birthday   Date of character creation
    """

    def __init__(self, header, user_id):
        """
        Initialize the class with data from API.

        :user_id: User ID for the represented Habitica user
        :header: HTTP header for accessing Habitica API
        """
        profile_data = utils.get_dict_from_api(
            header,
            "https://habitica.com/api/v3/members/{}".format(user_id))
        self.id = profile_data["_id"]  # pylint: disable=invalid-name
        self.displayname = profile_data["profile"]["name"]
        self.login_name = profile_data["auth"]["local"]["username"]
        self.habitica_birthday = datetime.strptime(
            profile_data["auth"]["timestamps"]["created"],
            "%Y-%m-%dT%H:%M:%S.%fZ")

    def __lt__(self, member):
        return self.id < member.id

    def __gt__(self, member):
        return self.id > member.id

    def __eq__(self, member):
        return self.id == member.id

    def __ge__(self, member):
        return self.id > member.id or self.id == member.id

    def __str__(self):
        """
        Return a string in format "Displayname (@loginname)".
        """
        return "{} (@{})".format(self.displayname, self.login_name)
