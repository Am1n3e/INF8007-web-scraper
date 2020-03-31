import os

from src.crawler import Crawler, CrawlerException
from src.file_scrapper import FileScrapper


class FileCrawler(Crawler):
    def __init__(self, file_path: str, show_exception_tb: bool) -> None:
        """Init the file crawler object.

        Args:
            file_path: The file path to crawl
            show_exception_tb: Enables exception trace back logging
        """
        super().__init__(file_path, show_exception_tb, True, -1, FileScrapper)

    def _get_root_route(self) -> str:
        return None  # For local file there is not root route

    def _verify_source_resource(self):
        if not os.path.isfile(self._resource):
            # If the file does not exists there is no need to continue
            raise CrawlerException(f"The source file ({self.__file_path}) does not exists")

    def _is_link_to_check(self, full_link):
        # Only external links can be checked when using a file
        return not FileCrawler._is_internal_link(full_link, None)

    def _create_full_link(self, source_link: str, link: str) -> str:
        if link is None:
            return source_link
        else:
            return link
