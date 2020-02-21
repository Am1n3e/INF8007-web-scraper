import logging
import requests

from src.scrapper import Scraper

logger = logging.getLogger(__name__)


class Crawler:
    def __init__(self, website_url: str) -> None:
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
    def dead_links(self) -> list:
        """Get the dead links.

        Returns:
            The dead links list
        """
        # Using a property to make sure that the dead links can't be modified (unless you mangle the name)
        return self.__dead_links

    def clear(self) -> None:
        """Clears the visited and dead links lists"""
        self.__visited_links = []
        self.__dead_links = []

    def crawl(self) -> None:
        """Crawl the website url given to the init"""
        self.clear()

        if Crawler._is_dead_link(self.__website_url):
            # If the web site is not accessible in the first place there is no need to continue
            raise ValueError(f"The source web page link ({self.__website_url}) is not accessible")

        self.__visited_links.append(self.__website_url)

        self._crawl(self.__website_url, "/")  # the "/" is for the root route (the website page it self)

        logger.info("Visited %d page(s)", len(self.__visited_links))

    def _crawl(self, source_link: str, route: str):
        """Crawl the page (source_link + route) given to the init"""
        full_link = self._create_full_link(source_link, route)
        links = Scraper.get_web_page_links(full_link)
        logger.debug("Crawling: %s. Found %d link(s)", full_link, len(links))

        for link in links:
            full_link = self._create_full_link(source_link, link)

            if not self._is_visited(full_link):

                self._mark_visited(full_link)

                if self._is_dead_link(full_link):
                    self._mark_dead(full_link)
                elif self._is_internal_link(link, source_link):
                    self._crawl(source_link, link)

    def _is_visited(self, link: str) -> bool:
        """Check if the link is already visited

        Args:
            link: The link to check

        Returns:
            True if the link is visited
        """
        # For advanced check, we can hash the body of page to exclude adds and un-used query parameters
        # But we felt that this would make a bigger project (to implement the right hashing function)
        return link in self.__visited_links

    def _mark_visited(self, link: str) -> None:
        """Mark the link as visited

        Args:
            link: The link to mark

        """
        self.__visited_links.append(link)

    def _mark_dead(self, link: str) -> None:
        """Mark the link as dead

        Args:
            link: The link to mark

        """
        self.__dead_links.append(link)

    @staticmethod
    def _is_internal_link(link: str, source_link: str) -> bool:
        """Check if link is internal

        Args:
            link: The link
            source_link: The source link

        Return:
            True if the link is internal else False
        """
        if link.startswith("/") or link.startswith(source_link):
            return True

        return False

    @staticmethod
    def _is_dead_link(link: str) -> bool:
        """Check if link is dead using the http response code

        Args:
            link: The link

        Return:
            True if the link is dead else False
        """
        try:
            response = requests.get(link)
            return response.status_code != 200  # Alive pages return 200 as http response status code
        except Exception as e:
            # This is to avoid stoping the app if one link is bad
            logger.error("Failed to check page status for %s. Bad regex or bad link", link)
            logger.exception(e)
            return True

    @staticmethod
    def _create_full_link(source_link: str, link: str) -> str:
        if link == "/":
            # root
            full_link = source_link
        elif link.startswith("/"):
            # internal links
            full_link = source_link + link
        else:
            # external links
            full_link = link

        if full_link.startswith("www"):
            # This is needed fo the python requests library. all links should be either http or https
            # We chose http, so the upstream will set to https in case it exists
            full_link = "http://" + full_link

        if full_link.endswith("/"):
            # Remove the trailing /,  so that http://hello.com/ and http://hello.com are the same
            full_link = full_link[:-1]

        return full_link
