
import click
import logging

logging.basicConfig(format='[%(asctime)s] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


@click.command()
@click.option('--photo-resolution', nargs=2, type=click.Tuple([int, int]), default=(1640, 1232))
@click.option('--debug', is_flag=True)
@click.option('--yes-gpio-pin', nargs=1, type=int, prompt=True)
@click.option('--no-gpio-pin', nargs=1, type=int, prompt=True)
@click.option('--debug', is_flag=True)
def main(photo_resolution, debug, yes_gpio_pin, no_gpio_pin):
    """
    Photo booth application for the Rapsberry Pi written in Python
    """

    logger = logging.getLogger()
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    from photoberry import PhotoBerryApplication
    app = PhotoBerryApplication()
    app.run(photo_resolution, yes_gpio_pin, no_gpio_pin)
