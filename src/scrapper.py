import re
import logging
import requests

logger = logging.getLogger(__name__)


class Scraper:
    @staticmethod
    def get_web_page_links(web_page_link: str) -> list:
        """Extract the links for a web page

        Args:
            web_page_link: The link to the web page

        Returns:
            The list of links
        """

        body = Scraper._get_page_body(web_page_link)

        # We use part of the regex proposed in https://stackoverflow.com/questions/6038061/regular-expression-to-find-urls-within-a-string

        text_and_href_links = re.findall(
            r"<a [\S]* ?href=[\'\"]?(/[^\'\"#>]+|http[s]?[^\r\n\t\f\v\"\']+)[\'\"]?|[^\'\"/](http[s]?://|www.)([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?",
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

    @staticmethod
    def _get_page_body(web_page_link: str) -> str:
        """Get the web page body

        Args:
            web_page_link: The link to the web page

        Returns:
            The body string
        """
        try:
            response = requests.get(web_page_link)
            response.raise_for_status()

        except Exception as e:
            # Raising an Exception, the scraper is expected to be called on an existing page
            logger.error("Failed to get page content for %s", web_page_link)
            logger.error(e)
            raise

        web_page_content = response.content.decode()

        # We choose to use the only since we don't care about programming links (css, schemas, ...)
        match = re.search(r"<body[^\>]*>([\s\S]*)<\/body>", web_page_content)
        if match is None:
            raise RuntimeError(f"Failed to extract web page body for {web_page_link}")
        body = match.groups()[0]

        return body
