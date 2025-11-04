from abc import ABC, abstractmethod

import requests


class CustomScraper(ABC):
    def __init__(self):
        pass

    def get_html_content(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
        }

        r = requests.get(url, headers=headers)

        if r.status_code == 200:

            return r.text

        raise RuntimeError(f"Failed to fetch website: {url}")

    @abstractmethod
    def scrape(self, url):
        pass
