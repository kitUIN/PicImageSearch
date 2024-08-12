from json import loads as json_loads

from lxml.html import HTMLParser, fromstring
from pyquery import PyQuery


class YandexItem:
    """Represents a single Yandex search result item.

    Holds details of a result from a Yandex reverse image search.

    Attributes:
        url: URL of the webpage with the image.
        title: Title or caption associated with the image.
        thumbnail: URL of the thumbnail image.
        source: Domain name of the website where the image was found.
        content: Additional text description or content with the image.
        size: Displayed dimensions or size information of the image.
    """

    def __init__(self, data: dict):
        """Initializes a YandexItem with data from a search result.

        Args:
            data: A dictionary containing the search result data.
        """
        self.origin: dict = data
        self.url: str = data["url"]
        self.title: str = data["title"]
        thumb_url: str = data["thumb"]["url"]
        self.thumbnail: str = (
            f"https:{thumb_url}" if thumb_url.startswith("//") else thumb_url
        )
        self.source: str = data["domain"]
        self.content: str = data["description"]
        original_image = data["originalImage"]
        self.size: str = f"{original_image['width']}x{original_image['height']}"


class YandexResponse:
    """Encapsulates a Yandex reverse image search response.

    Contains the complete response from a Yandex reverse image search operation.

    Attributes:
        raw: List of YandexItem instances for each search result.
        url: URL to the search results page.
    """

    def __init__(self, resp_text: str, resp_url: str):
        """Initializes with the response text and URL.

        Args:
            resp_text: the text of the response.
            resp_url: URL to the search result page.
        """
        utf8_parser = HTMLParser(encoding="utf-8")
        data = PyQuery(fromstring(resp_text, parser=utf8_parser))
        self.origin: PyQuery = data
        data_div = data.find('div.Root[id^="CbirSites_infinite"]')
        data_json = json_loads(data_div.attr("data-state"))
        sites = data_json["sites"]
        self.raw: list[YandexItem] = [YandexItem(site) for site in sites]
        self.url: str = resp_url
