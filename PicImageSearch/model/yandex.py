from typing import List

from lxml.html import HTMLParser, fromstring
from pyquery import PyQuery


class YandexItem:
    """A single Yandex search result item.

    Attributes:
        url: Direct URL of the image provided as a search result.
        title: Title associated with the image search result.
        thumbnail: URL of the image's thumbnail.
        source: Name of the source domain where the image was found.
        content: Description or any additional text content provided with the search result.
        size: The dimensions and/or size of the image found.
    """

    def __init__(self, data: PyQuery):
        """Initializes a YandexItem with data from a Yandex search result item.

        Args:
            data: A PyQuery object representing a search result item.
        """
        self.origin: PyQuery = data  # 原始数据 (raw data)
        self.url: str = data.find("div.CbirSites-ItemTitle a").attr("href")
        self.title: str = data.find("div.CbirSites-ItemTitle").text()
        self.thumbnail: str = data.find("div.CbirSites-ItemThumb img").attr("src")
        if not self.thumbnail:
            self.thumbnail = data.find("div.CbirSites-ItemThumb a").attr("href")
        if self.thumbnail and self.thumbnail.startswith("//"):
            self.thumbnail = f"https:{self.thumbnail}"
        self.source: str = data.find("a.CbirSites-ItemDomain").text()
        self.content: str = data.find("div.CbirSites-ItemDescription").text() or ""
        self.size: str = data.find("div.Thumb-Mark").text()


class YandexResponse:
    """Encapsulates the response from a Yandex reverse image search.

    Attributes:
        raw: A list of YandexItem objects representing the search results.
        url: The URL from which the search results were obtained.
    """

    def __init__(self, resp_text: str, resp_url: str):
        """Initializes a YandexResponse with data from a Yandex search response.

        Args:
            resp_text: The HTML text of the Yandex search response.
            resp_url: The URL of the Yandex search page.
        """
        utf8_parser = HTMLParser(encoding="utf-8")
        data = PyQuery(fromstring(resp_text, parser=utf8_parser))
        self.origin: PyQuery = data  # 原始数据 (raw data)
        # 结果返回值 (results returned from source)
        self.raw: List[YandexItem] = [
            YandexItem(i) for i in data.find("li.CbirSites-Item").items()
        ]
        self.url: str = resp_url
