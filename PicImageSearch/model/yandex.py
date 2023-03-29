from typing import List

from lxml.html import HTMLParser, fromstring
from pyquery import PyQuery


class YandexItem:
    def __init__(self, data: PyQuery):
        self.origin: PyQuery = data  # 原始数据
        self.url: str = data.find("div.CbirSites-ItemTitle a").attr("href")
        self.title: str = data.find("div.CbirSites-ItemTitle").text()
        self.thumbnail: str = data.find("div.CbirSites-ItemThumb img").attr("src")
        if not self.thumbnail:
            self.thumbnail = data.find("div.CbirSites-ItemThumb a").attr("href")
        if self.thumbnail and self.thumbnail.startswith("//"):
            self.thumbnail = "https:" + self.thumbnail
        self.source: str = data.find("a.CbirSites-ItemDomain").text()
        self.content: str = data.find("div.CbirSites-ItemDescription").text() or ""
        self.size: str = data.find("div.Thumb-Mark").text()


class YandexResponse:
    def __init__(self, resp_text: str, resp_url: str):
        utf8_parser = HTMLParser(encoding="utf-8")
        data = PyQuery(fromstring(resp_text, parser=utf8_parser))
        self.origin: PyQuery = data  # 原始数据
        # 结果返回值
        self.raw: List[YandexItem] = [
            YandexItem(i) for i in data.find("li.CbirSites-Item").items()
        ]
        self.url: str = resp_url
