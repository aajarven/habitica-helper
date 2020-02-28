"""
Tools for interacting with Habitica using the API.

The API calls follow the guidance in the Wiki page:
https://habitica.fandom.com/wiki/Guidance_for_Comrades#Rules_for_API_Calls
"""

from datetime import datetime
import requests


class PartyTool(object):
    """
    A class that provides methods for doing party-related things.
    """

    _timestamp_format = "%Y-%m-%dT%H:%M:%S.%fZ"

    def __init__(self, header):
        """
        Initialize the class.

        :header: Habitica requires specific fields to be present in all API
                 calls. This dict must contain them.
        """
        self._header = header

    def get_current_sharing_weekend(self):
        """
        Return the current sharing weekend challenge.

        The challenge is chosen based on the title containing words "Sharing
        Weekend Challenge" but not "TEMPLATE". If there are multiple, the one
        that has the most recent "created at" is returned.

        :returns: A dict representing the newest Sharing Weekend Challenge
        """
        response = requests.get(
            "https://habitica.com/api/v3/challenges/groups/party",
            headers=self._header)

        sharing_challenge = None
        for challenge in response.json()["data"]:
            if ("Sharing Weekend Challenge" not in challenge["name"] or
                    "TEMPLATE" in challenge["name"]):
                continue

            if not sharing_challenge:
                sharing_challenge = challenge
            else:
                old_created = datetime.strptime(sharing_challenge["createdAt"],
                                                self._timestamp_format)
                new_created = datetime.strptime(challenge["createdAt"],
                                                self._timestamp_format)
                if new_created > old_created:
                    sharing_challenge = challenge

        return sharing_challenge

    def get_challenge_participants(self, challenge_id):
        """
        Return a list of user_id's of all challenge participants.
        """
        user_ids = []
        last_id = None
        while True:
            url = "https://habitica.com/api/v3/challenges/{}/members".format(
                challenge_id
                )
            if last_id:
                url = "{}?lastId={}".format(url, last_id)
            response = requests.get(url, headers=self._header)
            data = response.json()["data"]

            for user in data:
                user_ids.append(user["id"])
            if len(data) < 30:
                break
            else:
                last_id = data[len(data) - 1]

        return user_ids
