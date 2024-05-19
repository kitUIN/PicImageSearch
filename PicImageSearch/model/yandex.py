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

    def __init__(self, data: PyQuery):
        """Initializes a YandexItem with data from a search result.

        Args:
            data: A PyQuery instance containing the search result item's data.
        """
        self.origin: PyQuery = data
        self.url: str = data.find("div.CbirSites-ItemTitle a").attr("href")
        self.title: str = data.find("div.CbirSites-ItemTitle").text()
        self.thumbnail: str = data.find("div.CbirSites-ItemThumb img").attr("src")
        if not self.thumbnail:
            self.thumbnail = data.find("div.CbirSites-ItemThumb a").attr("href")
        # Add https to thumbnail URL if protocol is missing
        if self.thumbnail and self.thumbnail.startswith("//"):
            self.thumbnail = f"https:{self.thumbnail}"
        self.source: str = data.find("a.CbirSites-ItemDomain").text()
        self.content: str = data.find("div.CbirSites-ItemDescription").text() or ""
        self.size: str = data.find("div.Thumb-Mark").text()


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
        self.raw: list[YandexItem] = [
            YandexItem(i) for i in data.find("li.CbirSites-Item").items()
        ]
        self.url: str = resp_url
