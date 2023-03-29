from typing import List

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
        glink = data.find(".glink")
        self.title = glink.text()
        if glink.parent("div"):
            self.url = glink.parent("div").parent("a").attr("href")
        else:
            self.url = glink.parent("a").attr("href")
        thumbnail = (
            data.find(".glthumb img")
            or data.find(".gl1e img")
            or data.find(".gl3t img")
        )
        self.thumbnail = thumbnail.attr("data-src") or thumbnail.attr("src")
        _type = data.find(".cs") or data.find(".cn")
        self.type = _type.eq(0).text()
        self.date = data.find("[id^='posted']").eq(0).text()
        self.tags = [
            i.text() for i in data.find("div[class=gt],div[class=gtl]").items()
        ]


class EHentaiResponse:
    def __init__(self, resp_text: str, resp_url: str):
        utf8_parser = HTMLParser(encoding="utf-8")
        data = PyQuery(fromstring(resp_text, parser=utf8_parser))
        self.origin: PyQuery = data  # 原始数据
        if "No unfiltered results found." in resp_text:
            self.raw = []
        else:
            tr_items = data.find(".itg").children("tr").items()
            if tr_items:
                self.raw = [EHentaiItem(i) for i in tr_items if i.children("td")]
            else:
                gl1t_items = data.find(".itg").children(".gl1t").items()
                self.raw = [EHentaiItem(i) for i in gl1t_items]
        self.url: str = resp_url
