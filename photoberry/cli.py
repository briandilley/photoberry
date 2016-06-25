import click

from photoberry import PhotoBerryApplication


@click.command()
def main():
    """Photo booth application for the Rapsberry Pi written in Python"""

    app = PhotoBerryApplication()
    app.run()
