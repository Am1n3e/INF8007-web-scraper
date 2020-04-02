import logging
import requests
import time
from typing import Tuple

from abc import ABC, abstractmethod

from src.scrapper import Scraper

logger = logging.getLogger(__name__)


class CrawlerException(Exception):
    pass


class Crawler(ABC):
    def __init__(
        self,
        resource: str,
        show_exception_tb: bool,
        disable_crawling: bool,
        trottle_duration_sec: int,
        scrapper: Scraper,
    ) -> None:
        """Init the crawler object.

        Args:
            website_url: The web site link to crawl
            show_exception_tb: Enables exception trace back logging
            disable_crawling: Disables crawling
            trottle: The trottle duration
        """
        # By using the '__' it will create a "private" var effect
        # Since mangling variables names is required to access the value
        self.__visited_links = []
        self.__dead_links = []
        self.__crawled_pages_cnt = 0
        self.__scrapper = scrapper

        self._resource = resource  # Act as protected member

        # for this var we don't care if the user change it
        self.trottle_duration_sec = trottle_duration_sec
        self.show_exception_tb = show_exception_tb
        self.disable_crawling = disable_crawling

    @property
    def dead_links(self) -> list:
        """Get the dead links.

        Returns:
            The dead links list
        """
        # Using a property to make sure that the dead links can't be modified (unless you mangle the name)
        return self.__dead_links

    @abstractmethod
    def _create_full_link(self, source_link: str, link: str) -> str:
        raise NotImplementedError()

    @abstractmethod
    def _is_link_to_check(self, full_link: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def _verify_source_resource(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def _get_root_route(self) -> str:
        return NotImplementedError()

    def clear(self) -> None:
        """Clears the visited and dead links lists"""
        self.__visited_links = []
        self.__dead_links = []
        self.__crawled_pages_cnt = 0

    def crawl(self) -> None:
        """Crawl the resource given to the init"""
        self.clear()

        self._verify_source_resource()

        self._crawl(self._resource, self._get_root_route())

        logger.info("Visited %d page(s)", len(self.__visited_links))

    def _crawl(self, source: str, route: str) -> None:
        """Crawl the page.

        Args:
            source: The page source
            route: The page route
        """
        self._check_trottle()

        full_link = self._create_full_link(source, route)
        links = self.__scrapper.get_links(full_link, self.show_exception_tb)

        logger.debug("Crawling: %s. Found %d link(s)", full_link, len(links))

        for link in links:
            full_link = self._create_full_link(source, link)

            if not self._is_visited(full_link):
                self._mark_visited(full_link)

                if self._is_link_to_check(full_link):
                    is_dead_link, status_code = self._is_dead_link(full_link)
                    logger.debug("Checking: %s %s", full_link, "Dead" if is_dead_link else "OK!")
                    if is_dead_link:
                        self._mark_dead(full_link, status_code)
                    elif not self.disable_crawling and self._is_internal_link(link, source):
                        self._crawl(source, link)

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

    def _mark_dead(self, link: str, error_status_code: int) -> None:
        """Mark the link as dead

        Args:
            link: The link to mark

        """
        self.__dead_links.append((link, error_status_code))

    @staticmethod
    def _is_internal_link(link: str, source_link: str) -> bool:
        """Check if link is internal

        Args:
            link: The link
            source_link: The source link

        Return:
            True if the link is internal else False
        """
        if link.startswith("/") or (source_link is not None and link.startswith(source_link)):
            return True

        return False

    def _is_dead_link(self, link: str) -> Tuple[str, str]:
        """Check if link is dead using the http response code

        Args:
            link: The link

        Return:
            (True, Reason) if the link is dead else (False, None)
        """

        try:
            response = requests.get(link)

            # Using "raise_for_status", the requests library will check if the status code
            # is within the valid range
            response.raise_for_status()

            return False, None
        except requests.exceptions.HTTPError as e:
            return True, f"Bad status code: {e.response.status_code} '{e.response.reason}'"
        except Exception as e:
            if self.show_exception_tb:
                logger.error("Error occured while checking %s", link, exc_info=True)

            # "Connection Error" is used to abstract the real error message sine it can be
            # Hard to read/understand. An advanced user can still see the origina exception
            # using the verbose mode.
            return True, "Connection error"

    def _check_trottle(self) -> None:
        """Check if a trottle is needed and sleep is yes"""
        self.__crawled_pages_cnt += 1

        if self.trottle_duration_sec > 0 and self.__crawled_pages_cnt % 10 == 0:
            logger.debug("Sleeping for %d", self.trottle_duration_sec)
            time.sleep(self.trottle_duration_sec)
