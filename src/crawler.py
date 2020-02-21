import requests

from src.scrapper import Scraper


class Crawler:
    def __init__(self, website_url):
        """Init the crawler object.

        Args:
            source_web_page_link: The web site link to crawl
        """
        # By using the '__' it will create a "private" var effect
        # Since mangling variables names is required to access the value
        self.__visited_links = []
        self.__dead_links = []
        self.__website_url = website_url

    @property
    def dead_links(self):
        """Get the dead links.

        Returns:
            The dead links list
        """
        # Using a property to make sure that the dead links can't be modified (unless you mangle the name)
        return self.__dead_links

    def clear(self):
        """Clears the visited and dead links lists"""
        self.__visited_links = []
        self.__dead_links = []

    def crawl(self):
        """Crawl the website url given to the init"""
        self.clear()

        if Crawler._is_dead_link(self.__website_url):
            # If the web site is not accessible in the first place there is no need to continue
            raise ValueError(f"The source web page link ({self.__website_url}) is not accessible")

        self.__visited_links.append(self.__website_url)

        self._crawl(self.__website_url, "/")  # the "/" is for the root route (the website page it self)

    def _crawl(self, source_link, route):
        """Crawl the page (source_link + route) given to the init"""
        links = Scraper.get_web_page_links(source_link + route)
        for link in links:
            full_link = source_link + link if link.startswith("/") else link
            if full_link not in self.__visited_links:
                self.__visited_links.append(full_link)

                if Crawler._is_dead_link(full_link):
                    self.__dead_links.append(full_link)
                elif link.startswith("/") or link.startswith(source_link):  # Internal links
                    self._crawl(source_link, link)

    @staticmethod
    def _is_dead_link(link):
        """Check if link is dead using the http response code

        Args:
            response: The link

        Return:
            True if the link is dead else False
        """
        response = requests.get(link)
        return response.status_code != 200  # Alive pages return 200 as http response status code
