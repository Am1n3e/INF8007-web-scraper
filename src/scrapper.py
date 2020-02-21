import re
import requests


class Scraper:
    @staticmethod
    def get_web_page_links(web_page_link: str):
        response = requests.get(web_page_link)

        if response.status_code != 200:
            # This function expext that link is not dead, so this is just to make sure upstream code is going the check
            raise RuntimeError(f"Unable to scrape {web_page_link}. Got status code = {response.status_code}")

        web_page_content = response.content.decode()

        match = re.search(r"<body[^\>]*>([\s\S]*)<\/body>", web_page_content)
        if match is None:
            raise RuntimeError(f"Failed to extract web page body for {web_page_link}")

        body = match.groups()[0]
        links = re.findall(r"<a [\S]* ?href=[\'\"]?(/[^\'\"#>]+|http[s]?[^\r\n\t\f\v\"\']+)[\'\"]?", body)

        return links
