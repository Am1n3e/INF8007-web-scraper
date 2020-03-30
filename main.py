import logging
import argparse

from tabulate import tabulate

from src.crawler import Crawler

logging.basicConfig()
logger = logging.getLogger(__name__)


def _parse_args():
    """Parse command line arguments

    Raises
        argparse error exceptions in case of missing or invalid args
    Returns:
        The command line args
    """
    arg_parser = argparse.ArgumentParser(description="Web crawler application")
    arg_parser.add_argument("website_url", help="Url of the website to crawl")
    arg_parser.add_argument("--verbose", action="store_true", help="Show debug messages")
    arg_parser.add_argument(
        "--trottle", type=int, help="Sleep time in secs between each 10 pages (to void rate limiters)", default=0
    )
    arg_parser.add_argument("--show_exception_tb", action="store_true", help="Show exception trace back")
    arg_parser.add_argument("--disable_crawling", action="store_true", help="Disable crawling (go depth of 1)")

    return arg_parser.parse_args()


def _print_dead_links(dead_links):
    """Print the dead links to console.

    Args:
        dead_links: The dead links list
    """
    if dead_links:
        table = tabulate(dead_links, headers=["Link", "Reason"])
        logger.info("dead links:\n%s", table)
    else:
        logger.info("No dead links found")


def _setup_logger(verbose):
    """Setup the root logger.
    Args:
        verbose: Flag to enable/disable debug message
    """
    logging.getLogger().setLevel(logging.DEBUG if verbose else logging.INFO)


def main():
    args = _parse_args()

    _setup_logger(args.verbose)
    try:
        crawler = Crawler(
            args.website_url,
            args.trottle,
            show_exception_tb=args.show_exception_tb,
            disable_crawling=args.disable_crawling,
        )
        crawler.crawl()

        _print_dead_links(crawler.dead_links)
    except Exception as exception:
        # Using Broad exception to catch all errors to give a proper error message
        logger.error("Error occured while crawling  %s", args.website_url)
        if args.show_exception_tb:  # To keep the output clean
            logger.exception(exception)

        exit(1)  # Useful when scripting the app

    exit(0)


if __name__ == "__main__":
    main()
