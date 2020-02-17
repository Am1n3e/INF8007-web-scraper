import re
import requests


class Scraper:
    @staticmethod
    def get_web_page_links(web_page_link: str, source_page: bool = False):
        response = requests.get(web_page_link)

        if Scraper._is_dead_link(response):
            if source_page:
                # If the page is not accessible there is no need to continue
                raise ValueError(f"The source web page link ({web_page_link}) is not accessible")

        web_page_content = response.content.decode()

        match = re.search(r"<body[^\>]*>([\s\S]*)<\/body>", web_page_content)
        if match is None:
            raise RuntimeError(f"Failed to extract web page body for {web_page_link}")

        body = match.groups()[0]
        links = re.findall(r"<a href=[\'\"]?(/[^\'\"#>]+|http[s]?[^\r\n\t\f\v\"\']+)[\'\"]?", body)

        return links

    @staticmethod
    def _is_dead_link(response: requests.Response):
        """Check if link is dead using the http response code

        Args:
            response: The http response

        Return:
            True if the link is dead else False
        """
        return response.status_code != 200


if __name__ == "__main__":
    links = Scraper.get_web_page_links("https://webscraper.io/test-sites/e-commerce/allinone")
    print(links)
