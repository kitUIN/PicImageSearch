from collections import namedtuple
from typing import List

from lxml.html import HTMLParser, fromstring
from pyquery import PyQuery

BASE_URL = "https://ascii2d.net"
SUPPORTED_SOURCES = ["pixiv", "twitter", "fanbox", "fantia", "ニコニコ静画", "ニジエ"]
URL = namedtuple("URL", ["href", "text"])


class Ascii2DItem:
    def __init__(self, data: PyQuery):
        self.origin: PyQuery = data  # 原始数据
        # 原图长宽，类型，大小
        self.hash: str = data("div.hash").eq(0).text()
        self.detail: str = data("small").eq(0).text()
        self.thumbnail: str = BASE_URL + data("img").eq(0).attr("src")
        self.url: str = ""
        self.url_list: List[URL] = []
        self.title: str = ""
        self.author: str = ""
        self.author_url: str = ""
        self._arrange(data)

    def _arrange(self, data: PyQuery) -> None:
        infos = data.find("div.detail-box.gray-link")
        if infos:
            links = infos.find("a")
            self.url_list = (
                [URL(i.attr("href"), i.text()) for i in links.items()] if links else []
            )
            mark = infos("small").eq(-1).text() if links else ""
            self._arrange_links(infos, links, mark)
            self._arrange_title(infos)
        self._normalize_url_list()
        if not self.url_list:
            self._arrange_backup_links(data)

    def _arrange_links(self, infos: PyQuery, links: PyQuery, mark: str) -> None:
        if links:
            link_items = list(links.items())
            if len(link_items) > 1 and mark in SUPPORTED_SOURCES:
                self.title, self.url = link_items[0].text(), link_items[0].attr("href")
                self.author_url, self.author = (
                    link_items[1].attr("href"),
                    link_items[1].text(),
                )
            elif links.eq(0).parents("small"):
                infos.remove("small")
                self.title = infos.text()

    def _arrange_title(self, infos: PyQuery) -> None:
        if not self.title:
            self.title = self._extract_external_text(infos) or infos.find("h6").text()
        if self.title and any(i in self.title for i in {"詳細掲示板のログ", "2ちゃんねるのログ"}):
            self.title = ""

    @staticmethod
    def _extract_external_text(infos: PyQuery) -> str:
        external = infos.find(".external")
        external.remove("a")
        return "\n".join((i.text() for i in external.items() if i.text())) or ""

    def _normalize_url_list(self) -> None:
        self.url_list = [
            URL(BASE_URL + url.href, url.text) if url.href.startswith("/") else url
            for url in self.url_list
        ]

    def _arrange_backup_links(self, data: PyQuery) -> None:
        links = data.find("div.pull-xs-right > a")
        if links:
            self.url = links.eq(0).attr("href")
            self.url_list = [URL(self.url, links.eq(0).text())]


class Ascii2DResponse:
    def __init__(self, resp_text: str, resp_url: str):
        utf8_parser = HTMLParser(encoding="utf-8")
        data = PyQuery(fromstring(resp_text, parser=utf8_parser))
        self.origin: PyQuery = data  # 原始数据
        # 结果返回值
        self.raw: List[Ascii2DItem] = [
            Ascii2DItem(i) for i in data.find("div.row.item-box").items()
        ]
        self.url: str = resp_url
