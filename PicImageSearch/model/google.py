from re import compile
from typing import Dict, List, Optional

from lxml.html import HTMLParser, fromstring
from pyquery import PyQuery


class GoogleItem:
    def __init__(self, data: PyQuery, thumbnail: Optional[str]):
        self.origin: PyQuery = data  # 原始数据
        self.title: str = data("h3").text()
        self.url: str = data("a").eq(0).attr("href")
        self.thumbnail: Optional[str] = thumbnail


class GoogleResponse:
    def __init__(self, resp_text: str, resp_url: str):
        utf8_parser = HTMLParser(encoding="utf-8")
        data = PyQuery(fromstring(resp_text, parser=utf8_parser))
        self.origin: PyQuery = data  # 原始数据
        self.page_number: int = 1  # 当前页
        self.url: str = resp_url
        index = 1
        for i, item in enumerate(
            list(data.find('div[role="navigation"] td').items())[1:-1]
        ):
            if not PyQuery(item).find("a"):
                index = i + 1
                self.page_number = int(PyQuery(item).text())
                break
        self.pages: List[str] = [
            f'https://www.google.com{i.attr("href")}'
            for i in data.find('a[aria-label~="Page"]').items()
        ]
        self.pages.insert(index - 1, resp_url)
        script_list = list(data.find("script").items())
        # 结果返回值
        thumbnail_dict: Dict[str, str] = self.create_thumbnail_dict(script_list)
        self.raw: List[GoogleItem] = [
            GoogleItem(i, thumbnail_dict.get(i('img[id^="dimg_"]').attr("id"), None))
            for i in data.find("#search .g").items()
        ]

    @staticmethod
    def create_thumbnail_dict(script_list: List[PyQuery]) -> Dict[str, str]:
        thumbnail_dict = {}
        base_64_regex = compile(r"data:image/(?:jpeg|jpg|png|gif);base64,[^'\"]+")
        id_regex = compile(r"dimg_\d+")

        for script in script_list:
            base_64_match = base_64_regex.findall(script.text())
            if not base_64_match:
                continue

            base64: str = base_64_match[0]
            id_list: List[str] = id_regex.findall(script.text())

            for _id in id_list:
                thumbnail_dict[_id] = base64.replace(r"\x3d", "=")

        return thumbnail_dict
