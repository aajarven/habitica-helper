"""
A tool for doing basic randomization when StockRandomizer is unavailable.
"""

import random


class BasicRandomizer(object):
    """
    A wrapper for python random module that Habitica challenge winners.
    """

    def pick_integer(self, min_, max_):
        """
        Return an integer between min (inclusive) and max (not inclusive).

        The value comes form an uniform distribution, and the seed is based on
        the stock and date given when initializing the class.

        :min_: Minimum value (inclusive)
        :max_: Maximum value (not inclusive)
        """
        return random.randint(min_, max_)
