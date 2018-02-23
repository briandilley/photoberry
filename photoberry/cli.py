
import click
import logging
import photoberry

logging.basicConfig(format='[%(asctime)s] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

default_print_command = 'lpr ' \
                        '-r ' \
                        '-o fit-to-page ' \
                        '-o position=center ' \
                        '{filename}'


@click.command()
@click.option('--photo-resolution', nargs=2, type=click.Tuple([int, int]), default=(1640, 1232))
@click.option('--strip-resolution-ratio', nargs=1, type=float, default=0.75)
@click.option('--debug', is_flag=True)
@click.option('--yes-gpio-pin', nargs=1, type=int, prompt=True)
@click.option('--no-gpio-pin', nargs=1, type=int, prompt=True)
@click.option('--print-command', nargs=1, type=str, default=default_print_command)
@click.option('--twitter-consumer-key', nargs=1, type=str)
@click.option('--twitter-consumer-secret', nargs=1, type=str)
@click.option('--twitter-access-token-key', nargs=1, type=str)
@click.option('--twitter-access-token-secret', nargs=1, type=str)
@click.option('--twitter-text', nargs=1, type=str, default="Created and uploaded with #photoberry")
@click.option('--twitter-disable-banner', is_flag=True, default=False)
@click.option('--disable-quit', is_flag=True)
@click.option('--debug', is_flag=True)
def main(photo_resolution, strip_resolution_ratio, debug, yes_gpio_pin, no_gpio_pin, print_command,
         twitter_consumer_key, twitter_consumer_secret, twitter_access_token_key, twitter_access_token_secret,
         twitter_text,
         twitter_disable_banner,
         disable_quit):
    """
    Photo booth application for the Rapsberry Pi written in Python
    """

    logger = logging.getLogger()
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    app = photoberry.PhotoBerryApplication(
        photo_resolution, strip_resolution_ratio,
        yes_gpio_pin, no_gpio_pin,
        print_command,
        disable_quit=disable_quit,
        twitter_credentials=photoberry.TwitterCredentials(
            twitter_consumer_key,
            twitter_consumer_secret,
            twitter_access_token_key,
            twitter_access_token_secret,
            twitter_text),
        twitter_disable_banner=twitter_disable_banner)

    app.run()
