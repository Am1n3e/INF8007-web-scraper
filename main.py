import argparse

from src.crawler import Crawler


def _parse_args():
    """Parse command line arguments

    Raises
        argparse error exceptions in case of missing or invalid args
    Returns:
        The command line args
    """
    arg_parser = argparse.ArgumentParser(description="Web crawler application")
    arg_parser.add_argument("website_url", help="Url of the website to crawl")

    return arg_parser.parse_args()


def _print_dead_links(dead_links):
    """Print the dead links to console.

    Args:
        dead_links: The dead links list
    """
    if dead_links:
        print(f'dead links: {" ".join(dead_links)}')
    else:
        print("No dead links found")


def main():
    args = _parse_args()

    try:
        crawler = Crawler(args.website_url)
        crawler.crawl()

        _print_dead_links(crawler.dead_links)
    except Exception as exception:
        # Using Broad excetion to catch all errors to give a proper error message
        print(f"Error occured while crawling {args.website_link}. {str(exception)}")


if __name__ == "__main__":
    main()
