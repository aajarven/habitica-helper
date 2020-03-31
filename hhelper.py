"""
Scripts for automating actions related to Habitica.
"""

from __future__ import print_function
import datetime
import click

from conf import calendars
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
    values of AEX index (Amsterdam Stock Exchange) from this week Tuesday. In
    order to make sure that the result is indeed deterministic, make sure that
    the stock has already closed for the day before calling the script:
    otherwise e.g. the closing price can still change.
    """
    tool = PartyTool(HEADER)
    challenge = tool.current_sharing_weekend()
    participants = tool.challenge_participants(challenge["id"])
    completers = sorted(tool.eligible_winners(challenge["id"], participants))

    click.echo("Eligible winners for challenge \"{}\" are:"
               "".format(challenge["name"].encode("utf-8")))
    for member in completers:
        click.echo(member.displayname)
    click.echo("")

    today = datetime.date.today()
    last_tuesday = today - datetime.timedelta(today.weekday() - 1)
    click.echo("Using stock data from {}".format(last_tuesday))

    rand = StockRandomizer("^AEX", last_tuesday)
    winner_index = rand.pick_integer(0, len(completers))
    click.echo("{} wins the challenge!".format(completers[winner_index]))

@cli.command()
def party_members():
    """
    Show current party members.
    """
    tool = PartyTool(HEADER)
    members = tool.party_members()
    for member in members:
        print(u"{:<20}(@{})".format(
            member.displayname.replace("\n", " "),
            member.login_name
            ))

@cli.command()
def party_birthdays():
    """
    Update party birthdays in the birthday calendar and print them.

    The birthdays are stored in the Google calendar whose ID is specified as
    BIRTHDAYS in conf/calendars.py.
    """
    tool = PartyTool(HEADER)
    members = tool.party_members()
    for member in members:
        bday = member.habitica_birthday
        result = tool.ensure_birthday(calendars.BIRTHDAYS, member)
        output = u"{:<20} {}.{}.{}\t{}".format(
            member.login_name,
            bday.day,
            bday.month,
            bday.year,
            result[1])
        click.echo(output)

if __name__ == "__main__":
    cli()
