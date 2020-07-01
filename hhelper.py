"""
Scripts for automating actions related to Habitica.
"""

from __future__ import print_function
import datetime
import click

from conf import calendars
from conf.header import HEADER
from habitica_helper.challenge import Challenge
from habitica_helper.habiticatool import PartyTool


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
    challenge_id = tool.current_sharing_weekend()["id"]
    challenge = Challenge(HEADER, challenge_id)

    click.echo(challenge.completer_str())
    click.echo("")

    today = datetime.date.today()
    last_tuesday = today - datetime.timedelta(today.weekday() - 1)

    click.echo(challenge.winner_str(last_tuesday, "^AEX"))


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


@cli.command()
@click.argument("challenge_name")
def participants(challenge_name):
    """
    Print list of everyone who completed CHALLENGE_NAME

    The given challenge name can be a substring of the whole name. If there are
    more than one matchin challenge, the newest one of them is returned.
    """
    tool = PartyTool(HEADER)
    challenge_id = tool.newest_matching_challenge([challenge_name], [])["id"]
    challenge = Challenge(HEADER, challenge_id)

    click.echo(challenge.completer_str())

if __name__ == "__main__":
    cli()
