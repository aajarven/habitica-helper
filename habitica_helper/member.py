"""
A class for representing Habitica user data.
"""

from datetime import datetime

from habitica_helper import utils


class Member():
    """
    Habitica user.

    Has the following attributes:
    id                  User ID
    displayname         Nickname shown to others
    login_name          Player handle used for logging in
    habitica_birthday   Date of character creation
    """

    def __init__(self, user_id, header=None, profile_data=None):
        """
        Initialize the class with data from API/dict.

        If header is provided, data is fetched from the api, otherwise given
        profile_data is used.

        :user_id: User ID for the represented Habitica user
        :header: HTTP header for accessing Habitica API
        :profile_data: Dict containing the following data:
                        id: UID for the user (str)
                        displayname: Display name (str)
                        loginname: Login name (str)
                        birthday: Habitica birthday (date)
        """
        if header:
            profile_data = utils.get_dict_from_api(
                header,
                "https://habitica.com/api/v3/members/{}".format(user_id))
            self.id = profile_data["_id"]  # pylint: disable=invalid-name
            self.displayname = profile_data["profile"]["name"]
            self.login_name = profile_data["auth"]["local"]["username"]
            self.habitica_birthday = datetime.strptime(
                profile_data["auth"]["timestamps"]["created"],
                "%Y-%m-%dT%H:%M:%S.%fZ")
        elif profile_data:
            self.id = profile_data["id"]
            self.displayname = profile_data["displayname"]
            self.login_name = profile_data["loginname"]
            self.habitica_birthday = profile_data["birthday"]
        else:
            raise AttributeError("Either header or profile_data must be "
                                 "provided for initializing a Member.")

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
