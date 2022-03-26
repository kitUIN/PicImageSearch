from typing import List

from pyquery import PyQuery


class GoogleItem:
    def __init__(self, data: PyQuery):
        self.origin: PyQuery = data  # 原始数据
        self.title: str = data("h3").text()
        self.url: str = data("a").eq(0).attr("href")
        self.thumbnail: str = ""
        thumbnail = data("img")
        if (
            thumbnail
            and thumbnail.attr("src")
            != "data:image/gif;base64,R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="
        ):
            self.thumbnail = thumbnail.attr("src")


class GoogleResponse:
    def __init__(self, data: PyQuery, pages: List[PyQuery], index: int):
        self.origin: PyQuery = data  # 原始数据
        # 结果返回值
        self.raw: List[GoogleItem] = [GoogleItem(i) for i in data.items()]
        self.index: int = index  # 当前页
        self.page: int = len(pages)  # 总页数
        self.pages: List[PyQuery] = pages  # 页面源

    def get_page_url(self, index: int) -> str:
        return f'https://www.google.com{self.pages[index - 1]("a").eq(0).attr("href")}'
