from typing import List

from lxml.html import HTMLParser, fromstring
from pyquery import PyQuery


class IqdbNorm:
    def __init__(self, data: PyQuery):
        self.origin: PyQuery = data  # 原始数据
        self.content: str = ""  # 备注
        self.url: str = ""
        self.source: str = ""  # 来源平台名称
        self.other_source: list = []  # 其他来源数据
        self.thumbnail: str = ""
        self.size: str = ""  # 原图长宽大小
        self.similarity: float = 0  # 相似值
        self._arrange(data)

    def _arrange(self, data: PyQuery):
        tr_list = list(data("tr").items())
        if len(tr_list) >= 5:
            self.content = tr_list[0]("th").text()
            if self.content == "No relevant matches":
                return
            tr_list = tr_list[1:]
        self.url = self._get_url(tr_list[0]("td > a").attr("href"))
        self.thumbnail = "https://iqdb.org" + tr_list[0]("td > a > img").attr("src")
        source_list = [i.tail.strip() for i in tr_list[1]("img")]
        self.source = source_list[0]
        other_source = tr_list[1]("td > a")
        if other_source:
            self.other_source.append(
                {
                    "source": source_list[1],
                    "url": self._get_url(other_source.attr("href")),
                }
            )
        self.size = tr_list[2]("td").text()
        similarity_raw = tr_list[3]("td").text()
        self.similarity = float(similarity_raw.replace("% similarity", ""))

    @staticmethod
    def _get_url(url: str):
        if url[:4] == "http":
            return url
        return f"https:{url}"


class IqdbResponse:
    def __init__(self, data: str):
        self.origin: str = data  # 原始数据
        self.raw: List[IqdbNorm] = []  # 结果返回值
        self.more: List[IqdbNorm] = []  # 更多结果返回值(低相似度)
        self.saucenao_url: str = ""  # SauceNao搜索链接
        self.ascii2d_url: str = ""  # Ascii2d搜索链接
        self.google_url: str = ""  # Google搜索链接
        self.tineye_url: str = ""  # TinEye搜索链接
        self._slice(data)

    def _slice(self, data: str) -> None:
        utf8_parser = HTMLParser(encoding="utf-8")
        d = PyQuery(fromstring(data, parser=utf8_parser))
        tables = list(d("#pages > div > table").items())
        if len(tables) > 1:
            self.raw.extend([IqdbNorm(i) for i in tables[1:]])
        content = tables[0].find("th").text()
        if content == "No relevant matches":
            self._get_other_urls(tables[0].find("a"))
        else:
            self._get_other_urls(d("#show1 > a"))
        self._get_more(d("#more1 > div.pages > div > table"))

    def _get_more(self, data: PyQuery) -> None:
        self.more.extend([IqdbNorm(i) for i in data.items()])

    def _get_other_urls(self, data: PyQuery) -> None:
        for link in data.items():
            if link.attr("href") == "#":
                continue
            if link.text() == "SauceNao":
                self.saucenao_url = "https:" + link.attr("href")
            elif link.text() == "ascii2d.net":
                self.ascii2d_url = link.attr("href")
            elif link.text() == "Google Images":
                self.google_url = "https:" + link.attr("href")
            elif link.text() == "TinEye":
                self.tineye_url = "https:" + link.attr("href")
