from lxml.html import HTMLParser, fromstring
from pyquery import PyQuery
import json


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
            data: A PyQuery instance containing the search result item's data.
        """

        self.origin: dict = data
        # Add https to thumbnail URL if protocol is missing
        if data["thumb"]["url"].startswith("//"):
            data["thumb"]["url"] = "https:" + data["thumb"]["url"]

        self.url: str = data["url"]
        self.title: str = data["title"]
        self.thumbnail: str = data["thumb"]["url"]
        self.source: str = data["domain"]
        self.content: str = data["description"]
        self.size: str = f"{data['originalImage']['width']}x{data['originalImage']['height']}"


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
        self.raw: list[YandexItem] = []
        data_json = json.loads(
            data.find('div.Root[id^="CbirSites_infinite"]').attr("data-state")
        )
        sites = data_json["sites"]
        for site in sites:
            self.raw.append(YandexItem(site))
        self.url: str = resp_url
