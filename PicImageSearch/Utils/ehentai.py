from typing import List

from httpx import Response
from lxml.html import HTMLParser, fromstring
from pyquery import PyQuery


class EHentaiItem:
    def __init__(self, data: PyQuery):
        self.origin: PyQuery = data  # 原始数据
        self.title: str = ""
        self.url: str = ""
        self.thumbnail: str = ""
        self.type: str = ""
        self.date: str = ""
        self.tags: List[str] = []
        self._arrange(data)

    def _arrange(self, data: PyQuery) -> None:
        self.title = data.find(".glink").text()
        self.url = data.find(".glink").parent("a").attr("href")
        self.thumbnail = data.find(".glthumb img").attr("src")
        self.type = data.find(".cn").eq(0).text()
        self.date = data.find("[id^='posted']").text()
        self.tags = [i.text() for i in data.find("div.gt").items()]


class EHentaiResponse:
    def __init__(self, resp: Response):
        self.origin: str = resp.text  # 原始数据
        utf8_parser = HTMLParser(encoding="utf-8")
        data = PyQuery(fromstring(self.origin, parser=utf8_parser))
        self.raw: List[EHentaiItem] = [
            EHentaiItem(i) for i in data.find(".glcat").parents("tr").items()
        ]
        self.url: str = str(resp.url)
