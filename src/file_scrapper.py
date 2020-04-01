import logging
from lxml import etree
from io import StringIO
from src.scrapper import Scraper

logger = logging.getLogger(__name__)


class FileScrapper(Scraper):
    @classmethod
    def _get_page_content(cls, resource: str, show_exception_tb: bool) -> str:
        """Get the page content

        Args:
            resource: The resource file path
            show_exception_tb: Enables exception trace back logging

        Returns:
            The page content string on success else returns an empty string
        """
        try:
            with open(resource, "r") as file_handle:
                web_page_content = file_handle.read()
        except Exception as e:
            # Raising an Exception, the scraper is expected to be called on an existing page
            logger.error("Failed to get page content for %s", resource)
            if show_exception_tb:
                logger.exception(e)
            return ""

        return cls._validate_html_file(resource, web_page_content, show_exception_tb)

    @classmethod
    def _validate_html_file(cls, file_path, content, show_exception_tb):
        try:
            etree.parse(StringIO(content), etree.HTMLParser(recover=False))
        except Exception as e:
            logger.error("Failed to get page content for %s. Invalid html file", file_path)
            if show_exception_tb:
                logger.exception(e)
            return ""

        return content
