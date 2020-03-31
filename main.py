import logging
import argparse
from tabulate import tabulate

from src.crawler import CrawlerException
from src.file_crawler import FileCrawler
from src.web_crawler import WebCrawler

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def _parse_args():
    """Parse command line arguments

    Raises
        argparse error exceptions in case of missing or invalid args
    Returns:
        The command line args
    """
    arg_parser = argparse.ArgumentParser(description="Web crawler application")
    subparsers = arg_parser.add_subparsers(help="Resource type")

    url_parser = subparsers.add_parser("url", help="Crawl URL. url -h for more details")
    url_parser.add_argument("resource", help="Url for the web page to crawl")
    url_parser.add_argument(
        "--trottle", type=int, help="Sleep time in secs between each 10 pages (to void rate limiters)", default=0
    )
    url_parser.set_defaults(func=_crawl_url)
    url_parser.add_argument("--disable_crawling", action="store_true", help="Disable crawling (go depth of 1)")

    file_parser = subparsers.add_parser("file", help="Crawl a file. file -h for more details")
    file_parser.add_argument("resource", help="file path of the html page to crawl")
    file_parser.set_defaults(func=_crawl_file)

    arg_parser.add_argument("--show_exception_tb", action="store_true", help="Show exception trace back")
    arg_parser.add_argument("--verbose", action="store_true", help="Show debug messages")

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
    # src: The python module is the name of the source folder
    logging.getLogger("src").setLevel(logging.DEBUG if verbose else logging.INFO)
    logging.getLogger(__name__).setLevel(logging.DEBUG if verbose else logging.INFO)


def _crawl(crawler, args):
    failure_occured = False
    try:
        crawler.crawl()
        _print_dead_links(crawler.dead_links)
    except CrawlerException as exception:
        logger.error(str(exception))
        failure_occured = True
    except Exception as exception:
        failure_occured = True
        # Using Broad exception to catch all errors to give a proper error message
        logger.error("Error occured while crawling  %s", args.resource)
        if args.show_exception_tb:  # To keep the output clean
            logger.exception(exception)

    exit(1 if failure_occured else 0)


def _crawl_url(args):
    crawler = WebCrawler(args.resource, args.show_exception_tb, args.trottle, args.disable_crawling)
    _crawl(crawler, args)


def _crawl_file(args):
    crawler = FileCrawler(args.resource, args.show_exception_tb)
    _crawl(crawler, args)


def main():
    args = _parse_args()

    _setup_logger(args.verbose)
    args.func(args)


if __name__ == "__main__":
    main()
