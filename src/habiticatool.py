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

    def current_sharing_weekend(self):
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

    def challenge_participants(self, challenge_id):
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

    def eligible_winners(self, challenge_id, user_ids):
        """
        Return a list of nicnames of eligible challenge winners.

        Here, anyone who has completed all todo type tasks is eligible: habits
        or dailies are not inspected.

        :challenge_id: ID of challenge for which eligibility is assessed.
        :user_ids: A list of IDs for users whose eligibility is to be tested.
        """
        eligible_winners = []
        for user_id in user_ids:
            response = requests.get(
                "https://habitica.com/api/v3/challenges/{}/members/{}"
                "".format(challenge_id, user_id),
                headers=self._header)
            progress_dict = response.json()["data"]
            eligible = True
            for task in progress_dict["tasks"]:
                if task["type"] == "todo" and not task["completed"]:
                    eligible = False
            if eligible:
                eligible_winners.append(progress_dict["profile"]["name"])
        return eligible_winners
