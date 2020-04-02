from src.crawler import Crawler, CrawlerException
from src.web_scrapper import WebScrapper


class WebCrawler(Crawler):
    def __init__(
        self, webpage_url: str, show_exception_tb: bool, trottle_duration_sec: int, disable_crawling: bool
    ) -> None:
        """Init the web crawler object.

        Args:
            web_page_url: The web page url to crawl
            show_exception_tb: Enables exception trace back logging
        """
        super().__init__(webpage_url, show_exception_tb, disable_crawling, trottle_duration_sec, WebScrapper)

    def _get_root_route(self) -> str:
        return "/"

    def _verify_source_resource(self):
        is_dead_link, _ = self._is_dead_link(self._resource)
        if is_dead_link:
            # If the web site is not accessible in the first place there is no need to continue
            raise CrawlerException(f"The source web page link ({self._resource}) is not accessible")

    def _is_link_to_check(self, full_link):
        # All link can be checked when using an URL
        return True

    def _create_full_link(self, source_link: str, link: str) -> str:
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
