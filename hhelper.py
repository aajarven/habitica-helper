"""
Scripts for automating actions related to Habitica.
"""

from __future__ import print_function
import click

from conf.header import HEADER
from src.habiticatool import PartyTool

@click.group()
def cli():
    """
    Command-line helpers for actions related to Habitica.
    """
    pass

@cli.command()
def sharing_winners():
    """
    Print nicks of all users who are eligible winners.

    This tool examines all participants in the newest sharing challenge, and
    prints ones that could win it. The newest challenge is picked automatically
    based on creation date, and everyone who has completed all todos is
    considered eligible to win.
    """
    tool = PartyTool(HEADER)
    challenge = tool.current_sharing_weekend()
    participants = tool.challenge_participants(challenge["id"])
    completers = tool.eligible_winners(challenge["id"], participants)

    click.echo("Eligible winners for challenge \"{}\" are:"
               "".format(challenge["name"]))
    for nick in completers:
        click.echo(nick)

if __name__ == "__main__":
    cli()
