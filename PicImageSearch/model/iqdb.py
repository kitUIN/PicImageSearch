from typing import Dict, List

from pyquery import PyQuery


class IqdbItem:
    def __init__(self, data: PyQuery):
        self.origin: PyQuery = data  # 原始数据
        self.content: str = ""  # 备注
        self.url: str = ""
        self.source: str = ""  # 来源平台名称
        self.other_source: List[Dict[str, str]] = []  # 其他来源数据
        self.thumbnail: str = ""
        self.size: str = ""  # 原图长宽大小
        self.similarity: float = 0  # 相似值
        self._arrange(data)

    def _arrange(self, data: PyQuery) -> None:
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
        self.similarity = float(similarity_raw.rstrip("% similarity"))

    @staticmethod
    def _get_url(url: str) -> str:
        if url[:4] == "http":
            return url
        return f"https:{url}"


class IqdbResponse:
    def __init__(self, data: PyQuery):
        self.origin: PyQuery = data  # 原始数据
        self.raw: List[IqdbItem] = []  # 结果返回值
        self.more: List[IqdbItem] = []  # 更多结果返回值(低相似度)
        self.saucenao_url: str = ""  # SauceNao搜索链接
        self.ascii2d_url: str = ""  # Ascii2d搜索链接
        self.google_url: str = ""  # Google搜索链接
        self.tineye_url: str = ""  # TinEye搜索链接
        self._arrange(data)

    def _arrange(self, data: PyQuery) -> None:
        tables = list(data("#pages > div > table").items())
        if len(tables) > 1:
            self.raw.extend([IqdbItem(i) for i in tables[1:]])
        content = tables[0].find("th").text()
        if content == "No relevant matches":
            self._get_other_urls(tables[0].find("a"))
        else:
            self._get_other_urls(data("#show1 > a"))
        self._get_more(data("#more1 > div.pages > div > table"))

    def _get_more(self, data: PyQuery) -> None:
        self.more.extend([IqdbItem(i) for i in data.items()])

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
