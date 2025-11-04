from typing import List, Type

from .custom_scraper import CustomScraper
from .wprm_scraper import WprmScraper


def custom_scraper_base_urls() -> List[str]:
    return WprmScraper.base_urls


def get_scrapper(url: str) -> Type[CustomScraper]:
    scraper = {url: WprmScraper for url in WprmScraper.base_urls}

    return scraper[url]
