import logging
from lxml import etree
from io import StringIO
from src.scrapper import Scraper

logger = logging.getLogger(__name__)


class HTMLScrapper(Scraper):
    # Pure function
    @classmethod
    def _get_page_content(cls, resource: str, show_exception_tb: bool) -> str:
        """Get the page content

        Args:
            resource: The html content
            show_exception_tb: Enables exception trace back logging

        Returns:
            The page content string on success else returns an empty string
        """
        return resource
