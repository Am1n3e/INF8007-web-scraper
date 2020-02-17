import argparse

from src.crawler import Crawler


def parse_args():
    arg_parser = argparse.ArgumentParser(description="Web crawler application")
    arg_parser.add_argument("website_link", help="link to website to crawl")

    return arg_parser.parse_args()


def main():
    args = parse_args()

    try:
        Crawler.crawl(args.website_link)
    except Exception as e:
        print(f"Error occured while crawling {args.website_link}. {str(e)}")


if __name__ == "__main__":
    main()
