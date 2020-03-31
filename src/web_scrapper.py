import logging
import requests

from src.scrapper import Scraper

logger = logging.getLogger(__name__)


class WebScrapper(Scraper):
    @classmethod
    def _get_page_content(cls, resource: str, show_exception_tb: bool) -> str:
        """Get the page content

        Args:
            resource: The resource web link 
            show_exception_tb: Enables exception trace back logging

        Returns:
            The page content string on success else returns an empty string
        """
        try:
            response = requests.get(resource)
            response.raise_for_status()

        except Exception as e:
            # Raising an Exception, the scraper is expected to be called on an existing page
            logger.error("Failed to get page content for %s", resource)
            if show_exception_tb:
                logger.exception(e)
            return ""

        return response.content.decode()
