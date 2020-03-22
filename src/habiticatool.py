"""
Tools for interacting with Habitica using the API.

The API calls follow the guidance in the Wiki page:
https://habitica.fandom.com/wiki/Guidance_for_Comrades#Rules_for_API_Calls
"""

from __future__ import print_function

from datetime import date, datetime
import requests

from src.google_calendar import GoogleCalendar

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

    def _get_dict_from_api(self, url):
        """
        Get data dict for API call represented by the given url.

        :url: URL for API get request
        :returns: Dict containing the data

        :raises: HTTPError if the request was bad
        """
        response = requests.get(url, headers=self._header)
        response.raise_for_status()
        return response.json()["data"]

    def _fetch_all_ids(self, url, pagelimit):
        """
        Return all user IDs returned by url, even from multiple pages.

        If not all users fit into one page returned by Habitica, a new query is
        run for the next page of users until all have been found.

        :url: Habitica API url for the interesting query
        :pagelimit: Maximum number of returned items per request.
        """
        user_ids = []
        last_id = None
        current_url = url
        while True:
            if last_id:
                current_url = "{}?lastId={}".format(url, last_id)
            data = self._get_dict_from_api(current_url)

            for user in data:
                user_ids.append(user["id"])
            if len(data) < pagelimit:
                break
            else:
                last_id = data[len(data) - 1]

        return user_ids

    def newest_matching_challenge(self, must_haves, no_gos):
        """
        Return the newest challenge with a name that fits the given criteria.

        The challenge is chosen based on its title containing all strings in
        the given must_haves iterable and none that are in no_gos. If there are
        multiple matching challenges, the one that has the most recent "created
        at" time is returned.

        :must_haves: iterable of strings that must be present in the name
        :no_gos: iterable of strings that must not be present in the name
        :returns: A dict representing the newest matching challenge
        """
        challenges = self._get_dict_from_api(
            "https://habitica.com/api/v3/challenges/groups/party")

        matching_challenge = None
        for challenge in challenges:
            name = challenge["name"]
            for substring in must_haves:
                if substring not in name:
                    continue
            for substring in no_gos:
                if substring in name:
                    continue

            if not matching_challenge:
                matching_challenge = challenge
            else:
                old_created = datetime.strptime(matching_challenge["createdAt"],
                                                self._timestamp_format)
                new_created = datetime.strptime(challenge["createdAt"],
                                                self._timestamp_format)
                if new_created > old_created:
                    matching_challenge = challenge

        return matching_challenge

    def current_sharing_weekend(self):
        """
        Return the current sharing weekend challenge.

        The challenge is chosen based on the title containing words "Sharing
        Weekend Challenge" but not "TEMPLATE". If there are multiple, the one
        that has the most recent "created at" is returned.

        :returns: A dict representing the newest Sharing Weekend Challenge
        """
        return self.newest_matching_challenge(
            ["Sharing Weekend"], ["TEMPLATE", "template", "Template"])

    def challenge_participants(self, challenge_id):
        """
        Return a list of user_id's of all challenge participants.
        """
        url = "https://habitica.com/api/v3/challenges/{}/members".format(
            challenge_id
            )

        return self._fetch_all_ids(url, 30)

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
            progress_dict = self._get_dict_from_api(
                "https://habitica.com/api/v3/challenges/{}/members/{}"
                "".format(challenge_id, user_id))
            eligible = True
            for task in progress_dict["tasks"]:
                if task["type"] == "todo" and not task["completed"]:
                    eligible = False
            if eligible:
                eligible_winners.append(progress_dict["profile"]["name"])
        return eligible_winners

    def party_members(self):
        """
        Return a dict with data of all party members.

        The dict uses the username as a key, the value of which is a dict
        containing "id", "displayname" and "habitica_birthday" as keys. The
        values of the two first are strings corresponding to user ID and
        display name of the user, and the last is the character creation
        timestamp as a datetime object.

        :returns: Dict with member data
        """
        member_ids = self._fetch_all_ids(
            "https://habitica.com/api/v3/groups/party/members",
            30)
        members = {}
        for member_id in member_ids:
            profile_url = ("https://habitica.com/api/v3/members/{}"
                           "".format(member_id))
            profile = self._get_dict_from_api(profile_url)
            bday = datetime.strptime(profile["auth"]["timestamps"]["created"],
                                     self._timestamp_format)
            login_name = profile["auth"]["local"]["username"]
            members[login_name] = {
                "id": member_id,
                "displayname": profile["profile"]["name"],
                "habitica_birthday": bday,
                }

        return members

    def add_birthdays(self, calendar_id):
        """
        Add Habitica birthdays of all party members to a Google calendar.
        """

        def _next_birthday(creationdate):
            """
            Return the date of the next birthday.

            :creationdate: datetime of character creation
            """
            today = date.today()
            this_year = today.year
            birthday_candidate = date(this_year, creationdate.month,
                                      creationdate.day)

            if birthday_candidate < today:
                return date(this_year + 1, creationdate.month,
                            creationdate.day)
            return birthday_candidate

        def _birthday_found(events, member):
            """
            Check whether the birthday of a member already has an event.

            :events: a list of events to be searched
            :member: the login name of membe for whom the events are checked
            :returns: True if birthday is present, otherwise False
            """
            for event in events:
                if member in event["summary"]:
                    return True
            return False

        calendar = GoogleCalendar(calendar_id)
        members = self.party_members()
        for member in members:
            creation = members[member]["habitica_birthday"]
            next_bday = _next_birthday(creation)
            bday_events = calendar.events_for_date(next_bday)
            if not _birthday_found(bday_events, member):
                title = "Habitica birthday of @{}".format(member)
                year_count = (next_bday.year -
                              members[member]["habitica_birthday"].year)
                description = (u"Celebrating the {} years {} has been a Habitician!"
                               u"".format(year_count,
                                          members[member]["displayname"]))
                calendar.insert_fullday_event(title, description, next_bday)
                print("Added birthday for @{}".format(member))
            else:
                print("Birthday event for @{} already present on {}.{}.{}"
                      "".format(member, next_bday.day, next_bday.month,
                                next_bday.year))
