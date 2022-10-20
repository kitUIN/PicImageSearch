from typing import List, Tuple

from lxml.html import HTMLParser, fromstring
from pyquery import PyQuery


class Ascii2DItem:
    def __init__(self, data: PyQuery):
        self.origin: PyQuery = data  # 原始数据
        # 原图长宽，类型，大小
        self.hash: str = data("div.hash").eq(0).text()
        self.detail: str = data("small").eq(0).text()
        self.thumbnail: str = "https://ascii2d.net" + data("img").eq(0).attr("src")
        self.url: str = ""
        self.url_list: List[Tuple[str, str]] = []
        self.title: str = ""
        self.author: str = ""
        self.author_url: str = ""
        self._arrange(data)

    def _arrange(self, data: PyQuery) -> None:
        infos = data.find("div.detail-box.gray-link")
        if infos:
            links = infos.find("a")
            if links:
                mark = infos("small").eq(-1).text()
                self.url_list = [(i.attr("href"), i.text()) for i in links.items()]
                if len(list(links.items())) > 1 and mark in [
                    "pixiv",
                    "twitter",
                    "fanbox",
                    "fantia",
                    "ニコニコ静画",
                    "ニジエ",
                ]:
                    self.title = links.eq(0).text()
                    self.url = links.eq(0).attr("href")
                    self.author_url = links.eq(1).attr("href")
                    self.author = links.eq(1).text()
                elif links.eq(0).parents("small"):
                    infos.remove("small")
                    self.title = infos.text()
            if not self.title:
                external = infos.find("div.external")
                external.remove("a")
                self.title = external.text()

        self.url_list = list(
            map(
                lambda x: (f"https://ascii2d.net{x[0]}", x[1])
                if x[0].startswith("/")
                else x,
                self.url_list,
            )
        )

        if not self.url_list:
            links = data.find("div.pull-xs-right > a")
            if links:
                self.url = links.eq(0).attr("href")
                self.url_list = [(self.url, links.eq(0).text())]


class Ascii2DResponse:
    def __init__(self, resp_text: str, resp_url: str):
        self.origin: str = resp_text  # 原始数据
        utf8_parser = HTMLParser(encoding="utf-8")
        data = PyQuery(fromstring(self.origin, parser=utf8_parser))
        # 结果返回值
        self.raw: List[Ascii2DItem] = [
            Ascii2DItem(i) for i in data.find("div.row.item-box").items()
        ]
        self.url: str = resp_url
