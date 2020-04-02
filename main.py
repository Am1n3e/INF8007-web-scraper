import re
import sys
import logging
import argparse
from tabulate import tabulate

from src.crawler import CrawlerException
from src.file_crawler import FileCrawler
from src.web_crawler import WebCrawler
from src.html_crawler import HTMLCrawler

logger = logging.getLogger(__name__)


def _parse_args():
    """Parse command line arguments

    Raises
        argparse error exceptions in case of missing or invalid args
    Returns:
        The command line args
    """
    arg_parser = argparse.ArgumentParser(description="Web crawler application")
    arg_parser.add_argument("--show_exception_tb", action="store_true", help="Show exception trace back")
    arg_parser.add_argument("--verbose", action="store_true", help="Show debug messages")
    arg_parser.add_argument(
        "--disable_crawling", action="store_true", help="Disable crawling (go depth of 1). only for urls"
    )
    arg_parser.add_argument(
        "--trottle",
        type=int,
        help="Sleep time in secs between each 10 pages (to void rate limiters). only for urls",
        default=0,
    )

    subparsers = arg_parser.add_subparsers(help="Resource type")

    url_parser = subparsers.add_parser("url", help="Crawl URL. url -h for more details")
    url_parser.add_argument("resource", help="Url for the web page to crawl")
    url_parser.set_defaults(func=_crawl_url)

    file_parser = subparsers.add_parser("file", help="Crawl a file. file -h for more details")
    file_parser.add_argument("resource", help="file path of the html page to crawl")
    file_parser.set_defaults(func=_crawl_file)

    std_in_parser = subparsers.add_parser("html", help="Crawl html content from stdin. html -h for more details")
    std_in_parser.add_argument("html_content", nargs="?", type=argparse.FileType("r"), default=sys.stdin)
    std_in_parser.set_defaults(func=_crawl_html)

    std_in_parser = subparsers.add_parser("file_list", help="Crawl file list from stdin. file_list -h for more details")
    std_in_parser.add_argument("file_list", nargs="?", type=argparse.FileType("r"), default=sys.stdin)
    std_in_parser.set_defaults(func=_crawl_file_list)

    std_in_parser = subparsers.add_parser("url_list", help="Crawl url list from stdin. url_list -h for more details")
    std_in_parser.add_argument("url_list", nargs="?", type=argparse.FileType("r"), default=sys.stdin)
    std_in_parser.set_defaults(func=_crawl_url_list)

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


def _setup_logger(logger_name, verbose):
    """Setup a logger.
    Args:
        logger_name: The logger name
        verbose: Flag to enable/disable debug message
    """
    main_logger = logging.getLogger(logger_name)
    main_logger.setLevel(logging.DEBUG if verbose else logging.INFO)

    format_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    out_stream = logging.StreamHandler(sys.stdout)
    out_stream.setLevel(logging.DEBUG)
    out_stream.setFormatter(logging.Formatter(format_str))
    # The filter help to select only the messages with level info or bellow to go
    # to stdout
    out_stream.addFilter(lambda record: record.levelno <= logging.INFO)

    error_stream = logging.StreamHandler(sys.stderr)
    error_stream.setLevel(logging.ERROR)
    error_stream.setFormatter(logging.Formatter(format_str))

    main_logger.addHandler(out_stream)
    main_logger.addHandler(error_stream)


def _setup_loggers(verbose):
    """Setup the application loggers.
    Args:
        verbose: Flag to enable/disable debug message
    """
    _setup_logger(__name__, verbose)  # __name__: The current module
    _setup_logger("src", verbose)  # src: The python module is the name of the source folder


def _print_header(resource):
    print("*" * 100)
    print("*" * 100)
    print(resource)
    print("*" * 100)


def _crawl(crawler, args, do_exit=True):
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
        logger.error("Error occured while crawling")
        if args.show_exception_tb:  # To keep the output clean
            logger.exception(exception)

    exit_code = 1 if failure_occured else 0
    if do_exit:
        sys.exit(exit_code)
    else:
        return exit_code


def _crawl_url(args):
    crawler = WebCrawler(args.resource, args.show_exception_tb, args.trottle, args.disable_crawling)
    _crawl(crawler, args)


def _crawl_file(args):
    crawler = FileCrawler(args.resource, args.show_exception_tb)
    _crawl(crawler, args)


def _crawl_html(args):
    crawler = HTMLCrawler(args.html_content.read(), args.show_exception_tb)
    _crawl(crawler, args)


def _crawl_resource_list(resource_list, args, create_crawler):
    over_all_exit_code = 0
    for resource in resource_list:
        _print_header(resource)
        crawler = create_crawler(resource, args)
        exit_code = _crawl(crawler, args, do_exit=False)
        if exit_code == 1:
            over_all_exit_code = 1

    sys.exit(over_all_exit_code)


def _crawl_url_list(args):
    def create_crawler(resource, args):
        return WebCrawler(resource, args.show_exception_tb, args.trottle, args.disable_crawling)

    url_list = re.split(r"\s+", args.url_list.read().strip())
    _crawl_resource_list(url_list, args, create_crawler)


def _crawl_file_list(args):
    def create_crawler(resource, args):
        return FileCrawler(resource, args.show_exception_tb)

    file_list = re.split(r"\s+", args.file_list.read().strip())
    _crawl_resource_list(file_list, args, create_crawler)


def main():
    args = _parse_args()

    _setup_loggers(args.verbose)

    args.func(args)


if __name__ == "__main__":
    main()
