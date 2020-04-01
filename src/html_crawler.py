from src.crawler import Crawler
from src.html_scraper import HTMLScrapper


class HTMLCrawler(Crawler):
    def __init__(self, html_content: str, show_exception_tb: bool) -> None:
        """Init the html crawler object.

        Args:
            html_content: The html content
            show_exception_tb: Enables exception trace back logging
        """
        super().__init__(html_content, show_exception_tb, True, -1, HTMLScrapper)

    def _get_root_route(self) -> str:
        return None  # For local file there is not root route

    def _verify_source_resource(self):
        pass

    def _is_link_to_check(self, full_link):
        # Only external links can be checked when using a file
        return not self._is_internal_link(full_link, None)

    def _create_full_link(self, source_link: str, link: str) -> str:
        if link is None:
            return source_link
        else:
            return link
