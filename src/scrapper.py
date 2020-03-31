import re
import logging
import requests
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class Scraper(ABC):
    @classmethod
    def get_links(cls, resource: str, show_exception_tb: bool) -> list:
        """Extract the links for the resource

        Args:
            resource: The resource to parse
            show_exception_tb: Enables exception trace back logging

        Returns:
            The list of links
        """

        body = cls._get_body(resource, show_exception_tb)

        # We use part of the regex proposed in https://stackoverflow.com/questions/6038061/regular-expression-to-find-urls-within-a-string
        text_and_href_links = re.findall(
            r"<a [\S]* ?href=[\'\"]?(/[^\'\">]+|http[s]?[^\r\n\t\f\v\"\']+)[\'\"]?|[^\'\"/](http[s]?://|www.)([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?",
            body,
        )

        links = []
        for item in text_and_href_links:
            href_links = item[0]
            if href_links:
                links.append(href_links)
            if item[1]:
                # Happens for text url. To make the python regexp work we used gourps
                links.append(item[1] + item[2] + item[3])

        return links

    @classmethod
    def _get_body(cls, resource: str, show_exception_tb: bool) -> str:
        """Get the page body

        Args:
            resource: The resource to extract the body from

        Returns:
            The body string
        """
        page_content = cls._get_page_content(resource, show_exception_tb)

        # We choose to use the only since we don't care about programming links (css, schemas, ...)
        match = re.search(r"<body[^\>]*>([\s\S]*)<\/body>", page_content)
        if match is None:
            logger.error("Failed to extract web page body for %s", page_content)
            return ""

        body = match.groups()[0]

        return body

    @classmethod
    @abstractmethod
    def _get_page_content(cls, resource, show_exception_tb):
        raise NotImplementedError()
