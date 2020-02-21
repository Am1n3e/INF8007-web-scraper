import argparse

from src.crawler import Crawler


def parse_args():
    arg_parser = argparse.ArgumentParser(description="Web crawler application")
    arg_parser.add_argument("website_url", help="Url of the website to crawl")

    return arg_parser.parse_args()


def main():
    args = parse_args()

    try:
        crawler = Crawler(args.website_url)
        crawler.crawl()
        print(f'dead links: {" ".join(crawler.dead_links)}')
    except Exception as exception:
        # Using Broad excetion to catch all errors to give a proper error message
        print(f"Error occured while crawling {args.website_link}. {str(exception)}")


if __name__ == "__main__":
    main()
