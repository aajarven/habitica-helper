"""
A tool for doing confirmable random selection based on public data.
"""

from datetime import timedelta
from math import modf
import random
import yfinance as yf


class StockRandomizer(object):
    """
    A wrapper for python random module that picks seed based on stocks.

    This means that the fairness of the selection can be verified but it cannot
    be predicted before the date of the stock data retrieval.
    """

    def __init__(self, ticker, date):
        """
        Initialize the randomizer with a stock-based seed.

        :ticker: The stock symbol used by Yahoo! finance
        :date: Datetime of the day to be used
        """
        random.seed(self._stock_seed(ticker, date))

    def pick_integer(self, min_, max_):
        """
        Return an integer between min (inclusive) and max (not inclusive).

        The value comes form an uniform distribution, and the seed is based on
        the stock and date given when initializing the class.

        :min_: Minimum value (inclusive)
        :max_: Maximum value (not inclusive)
        """
        return random.randint(min_, max_)

    def _stock_seed(self, ticker, date):
        """
        Sets the rng seed to a value between 0 and 99999999 based on stocks.

        The value consists of two decimals of the opening, closing, highest and
        lowest values of the given stock for the given day, concatenated in
        that order.

        :ticker: The stock symbol used by Yahoo! finance
        :date: Datetime of the day to be used
        """
        stock = yf.Ticker(ticker)
        data = stock.history(start=date, end = date + timedelta(days=1))
        keys = ["Open", "High", "Low", "Close"]
        seed = 0
        for index, key in enumerate(keys):
            decimals, _ = modf(data.iloc[0][key])
            seed = seed*100 + int(round(decimals*100))
        print "Using seed {}".format(seed)
        return seed
