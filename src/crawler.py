import requests

from src.scrapper import Scraper


class Crawler:
    @staticmethod
    def crawl(source_web_page_link):
        website_links = {"visited": [], "dead": []}

        website_links["visited"].append(source_web_page_link)

        if Crawler._is_dead_link(source_web_page_link):
            # If the page is not accessible there is no need to continue
            raise ValueError(f"The source web page link ({source_web_page_link}) is not accessible")

        Crawler._crawl(source_web_page_link, "/", website_links)

        return website_links["dead"]

    @staticmethod
    def _crawl(source_web_page_link, route, website_links):
        links = Scraper.get_web_page_links(source_web_page_link + route)
        for link in links:
            full_link = source_web_page_link + link if link.startswith("/") else link
            if full_link not in website_links["visited"]:

                website_links["visited"].append(full_link)

                if Crawler._is_dead_link(full_link):
                    website_links["dead"].append(link)
                elif link.startswith("/") or link.startswith(source_web_page_link):  # Internal links
                    Crawler._crawl(source_web_page_link, link, website_links)

    @staticmethod
    def _is_dead_link(link):
        """Check if link is dead using the http response code

        Args:
            response: The link

        Return:
            True if the link is dead else False
        """
        response = requests.get(link)
        return response.status_code != 200


if __name__ == "__main__":
    print(Crawler.crawl("https://webscraper.io"))
