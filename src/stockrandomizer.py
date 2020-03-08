"""
A tool for doing confirmable random selection based on public data.
"""

import yfinance as yf


class StockRandomizer(object):
    """
    TODO
    """

    def _get_stock_seed(self, ticker):
        stock = yf.Ticker(ticker)
        print stock.history(start="2020-03-01", end="2020-03-08")
