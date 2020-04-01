import logging
from lxml import etree
from io import StringIO
from src.scrapper import Scraper

logger = logging.getLogger(__name__)


class HTMLScrapper(Scraper):
    @classmethod
    def _get_page_content(cls, resource: str, show_exception_tb: bool) -> str:
        """Get the page content

        Args:
            resource: The html content
            show_exception_tb: Enables exception trace back logging

        Returns:
            The page content string on success else returns an empty string
        """
        return cls._validate_html_content(resource, show_exception_tb)

    @classmethod
    def _validate_html_content(cls, content, show_exception_tb):
        try:
            etree.parse(StringIO(content), etree.HTMLParser(recover=False))
        except Exception as e:
            logger.error("Failed to get html content from stdin. Invalid html file")
            if show_exception_tb:
                logger.exception(e)
            return content

        return content
