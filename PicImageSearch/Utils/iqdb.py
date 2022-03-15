import re
from typing import List

from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag


class IqdbNorm:
    iqdb_url = "https://iqdb.org"

    def __init__(self, data: Tag, isnot_more: bool = True):
        self.isnot_more: bool = isnot_more
        """"""
        self.content: str = "None"
        """备注"""
        self.url: str = "None"
        """url地址"""
        self.source: str = "None"
        """来源平台名称"""
        self.other_source: list = list()
        """其他来源"""
        self.thumbnail: str = "None"
        """缩略图地址"""
        self.size: str = "None"
        """原图长宽大小"""
        self.similarity: str = "None"
        """	相似值"""
        self._arrange(data.table)

    def _arrange(self, data: Tag):
        regex_iq = re.compile("[0-9]+")
        if self.isnot_more:
            self.content = data.tr.th.string
            if self.content == "No relevant matches":
                return
            # logger.info(self.content)
            tbody = data.tr.next_sibling
        else:
            tbody = data.tr
        self.url = (
            tbody.td.a["href"]
            if tbody.td.a["href"][:4] == "http"
            else "https:" + tbody.td.a["href"]
        )
        self.thumbnail = self.iqdb_url + tbody.td.a.img["src"]
        tbody = tbody.next_sibling
        source = [stt for stt in tbody.td.strings]
        if len(source) > 1:
            self.other_source.append(
                {
                    "source": source[1],
                    "url": tbody.td.a["href"]
                    if tbody.td.a["href"][:4] == "http"
                    else "https:" + tbody.td.a["href"],
                }
            )
        tbody = tbody.next_sibling
        self.size = tbody.td.string
        similarity_raw = regex_iq.search(tbody.next_sibling.td.string)
        if similarity_raw:
            self.similarity = similarity_raw.group(0) + "%"
        self.source = source[0]

    def __repr__(self):
        return f"<NormIqdb(content={repr(self.content)}, title={repr(self.source)}, similarity={repr(self.similarity)}>"


class IqdbResponse:
    def __init__(self, res: bytes):
        self.origin: bytes = res
        """原始返回值"""
        # logger.info(type(self.origin))
        self.raw: List[IqdbNorm] = list()
        """结果返回值"""
        self.more: List[IqdbNorm] = list()
        """更多结果返回值(低相似度)"""
        self.saucenao: str = "None"
        """SauceNao搜索链接"""
        self.ascii2d: str = "None"
        """Ascii2d搜索链接"""
        self.google: str = "None"
        """Google搜索链接"""
        self.tineye: str = "None"
        """TinEye搜索链接"""
        self._slice(res)

    def _slice(self, data: bytes) -> None:
        soup: BeautifulSoup = BeautifulSoup(data, "html.parser")

        pages = soup.find(attrs={"class": "pages"})
        for i in pages:
            if i == "\n" or str(i) == "<br/>" or "Your image" in str(i):
                continue
            # logger.info(i)
            self.raw.append(IqdbNorm(i))
        self._get_show(soup.find(attrs={"id": "show1"}))
        self._get_more(soup.find(attrs={"id": "more1"}))

    def _get_more(self, data: Tag) -> None:
        for i in data.contents[2]:
            if str(i)[:2] == "<d":
                self.more.append(IqdbNorm(i, False))
            # logger.info(i)

    def _get_show(self, data: Tag) -> None:
        for j in data.contents:
            if type(j) != NavigableString:
                if j["href"] == "#":
                    continue
                if j.string == "SauceNao":
                    self.saucenao = "https:" + j["href"]
                elif j.string == "ascii2d.net":
                    self.ascii2d = j["href"]
                elif j.string == "Google Images":
                    self.google = "https:" + j["href"]
                elif j.string == "TinEye":
                    self.tineye = "https:" + j["href"]

    def __repr__(self):
        return f"<IqdbResponse(count={repr(len(self.raw))})>"
