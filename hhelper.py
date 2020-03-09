"""
Scripts for automating actions related to Habitica.
"""

from __future__ import print_function
import datetime
import click

from conf.header import HEADER
from src.habiticatool import PartyTool
from src.stockrandomizer import StockRandomizer

@click.group()
def cli():
    """
    Command-line helpers for actions related to Habitica.
    """
    pass

@cli.command()
def sharing_winners():
    """
    Pick winner from amongst all users who are eligible winners.

    This tool examines all participants in the newest sharing challenge, and
    prints ones that could win it. The newest challenge is picked automatically
    based on creation date, and everyone who has completed all todos is
    considered eligible to win.

    The winner is chosen based on the opening, closing, highest and lowest
    values of AEX index (Amsterdam Stock Exchange) from the previous monday.
    """
    tool = PartyTool(HEADER)
    challenge = tool.current_sharing_weekend()
    participants = tool.challenge_participants(challenge["id"])
    completers = tool.eligible_winners(challenge["id"], participants)

    click.echo("Eligible winners for challenge \"{}\" are:"
               "".format(challenge["name"].encode("utf-8")))
    for nick in completers:
        click.echo(nick)
    click.echo("")

    today = datetime.date.today()
    last_monday = today - datetime.timedelta(today.weekday())
    click.echo("Using stock data from {}".format(last_monday))

    rand = StockRandomizer("^AEX", last_monday)
    winner_index = rand.pick_integer(0, len(completers))
    click.echo("{} wins the challenge!".format(completers[winner_index]))

if __name__ == "__main__":
    cli()
