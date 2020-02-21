import re
import logging
import requests

logger = logging.getLogger(__name__)


class Scraper:
    @staticmethod
    def get_web_page_links(web_page_link: str):
        """Extract the links for a web page

        Args:
            web_page_link: The link to the web page

        Returns:
            The list of links
        """

        body = Scraper._get_page_body(web_page_link)

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
    def _get_page_body(web_page_link):
        """Get the web page body

        Args:
            web_page_link: The link to the web page

        Returns:
            The body string
        """
        try:
            response = requests.get(web_page_link)
        except Exception as e:
            # This is to avoid stoping the app if one link is bad
            logger.error("Failed to check page content for %s. Bad regex or bad link", web_page_link)
            logger.exception(e)

        if response.status_code != 200:
            # This function expext that link is not dead, so this is just to make sure upstream code is going the check
            logger.error(f"Unable to scrape {web_page_link}. Got status code = {response.status_code}")

        web_page_content = response.content.decode()

        # We choose to use the only since we don't care about programming links (css, schemas, ...)
        match = re.search(r"<body[^\>]*>([\s\S]*)<\/body>", web_page_content)
        if match is None:
            raise RuntimeError(f"Failed to extract web page body for {web_page_link}")
        body = match.groups()[0]

        return body
