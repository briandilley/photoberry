import click

from photoberry import PhotoBerryApplication


@click.command()
@click.option('--preview-resolution', nargs=2, type=click.Tuple([int, int]), default=(800, 600))
def main(preview_resolution=None):
    """Photo booth application for the Rapsberry Pi written in Python"""

    app = PhotoBerryApplication()
    app.preview_resolution = preview_resolution
    app.run()
