import click

from photoberry import PhotoBerryApplication

import logging
logging.basicConfig(format='[%(asctime)s] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


@click.command()
@click.option('--photo-resolution', nargs=2, type=click.Tuple([int, int]), default=(1024, 768))
@click.option('--debug', is_flag=True)
def main(photo_resolution, debug):
    """
    Photo booth application for the Rapsberry Pi written in Python
    """

    logger = logging.getLogger()
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    app = PhotoBerryApplication()
    app.run(photo_resolution)
