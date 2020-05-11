"""
A class for representing a Habitica challenge.
"""

from habitica_helper.habiticatool import PartyTool
from habitica_helper.stockrandomizer import StockRandomizer
from habitica_helper import utils


class Challenge(object):
    """
    TODO
    """  # TODO

    def __init__(self, header, challenge_id):
        """
        Create a class for a challenge.

        :header: Header to use with API
        :challenge_id: The ID of the represented challenge
        """
        self.id = challenge_id
        self._full_data = utils.get_dict_from_api(
            header,
            "https://habitica.com/api/v3/challenges/{}".format(challenge_id))
        self._party_tool = PartyTool(header)
        self._participants = None
        self._completers = None
    
    @property
    def participants(self):
        """
        A list of all party members who have joined the challenge.
        """
        if self._participants is None:
            self._participants = self._party_tool.challenge_participants(
                self.id)
        return self._participants

    @property
    def completers(self):
        """
        A list of party members who have completed all challenge todo tasks.
        """
        if self._completers is None:
            self._completers = sorted(self._party_tool.eligible_winners(
                self.id, self.participants))
        return self._completers

    @property
    def name(self):
        """
        The name of the challenge.
        """
        return self._full_data["name"]

    @name.setter
    def name(self, name):
        """
        Rename the challenge.

        This method only affects the local copy of the challenge: the update()
        method needs to be called to send the changes to Habitica.
        """
        self._full_data["name"] = name

    @property
    def summary(self):
        """
        The challenge summary.
        """
        return self._full_data["summary"]

    @summary.setter
    def summary(self, summary):
        """
        Change the summary of the challenge.

        This method only affects the local copy of the challenge: the update()
        method needs to be called to send the changes to Habitica.
        """
        self._full_data["summary"] = summary

    @property
    def description(self):
        """
        The challenge description.
        """
        return self._full_data["description"]

    @description.setter
    def description(self, description):
        """
        Change the challenge description.

        This method only affects the local copy of the challenge: the update()
        method needs to be called to send the changes to Habitica.
        """
        self._full_data["description"] = description

    def update(self):
        """
        Update the name, description and summary of the challenge.
        """
        new_data = {"name": self.name,
                    "description": self.description,
                    "summary": self.summary}
        requests.put(
            "https://habitica.com/api/v3/challenges/{}".format(self.id),
            data=new_data, headers=self.header)

    def completer_str(self):
        """
        Return a string listing all people who completed the challenge
        """
        if len(self.completers) == 0:
            return ("Nobody completed all tasks for challenge \"{}\"."
                    "".format(self.name))

        intro = ("The party members who completed all todo tasks for "
                 "challenge \"{}\" are:\n".format(self.name))
        completer_lines = ["- {}".format(member.displayname)
                          for member in self.completers]
        return intro + "\n".join(completer_lines)

    def winner(self, date, stock):
        """
        Pick a winner for the challenge, based on the values of stock on a date

        :date: Date object representing the date from which to use the stock
               data.
        :stock: Stock to use, e.g. "^AEX". Make sure that the stock has already
                closed for the day used: otherwise the result might still
                change.
        :returns: The Member who won the challenge
        """
        randomizer = StockRandomizer(stock, date)
        winner_index = randomizer.pick_integer(0, len(self.completers))
        return self.completers[winner_index]

    def winner_str(self, date, stock):
        """
        Pick a winner as `winner` does, but return a string.

        The returned string states the date, stock and seed used to pick the
        winner, together with the name of the winner.

        :date: Date object representing the date from which to use the stock
               data.
        :stock: Stock to use, e.g. "^AEX". Make sure that the stock has already
                closed for the day used: otherwise the result might still
                change.
        :returns: A string describing the process.
        """
        randomizer = StockRandomizer(stock, date)
        winner = self.winner(date, stock)
        return ("Using stock data for {} from {} (seed {}).\n\n"
                "{} wins the challenge!".format(date, stock, randomizer.seed, winner))

    def clone(self):
        """
        Create a clone of this challenge and return its ID.
        """
        resp = requests.post("https://habitica.com/api/v3/challenges/{}/clone"
                             "".format(self._id), headers=self.header)
        resp.raise_for_status
        return resp.json()["data"]["id"]
