from typing import List
from re import compile
from json import dump

from pyquery import PyQuery


class GoogleItem:
    def __init__(self, data: PyQuery, thumbnail: str):
        self.origin: PyQuery = data  # 原始数据
        self.title: str = data("h3").text()
        self.url: str = data("a").eq(0).attr("href")
        self.thumbnail: str = thumbnail

class GoogleResponse:
    def __init__(self, data: PyQuery, pages: List[PyQuery], index: int, images_data: PyQuery):
        self.origin: PyQuery = data  # 原始数据
        # 结果返回值
        thumbnail: dict = self.create_list_thumbnail(images_data)
        self.raw: List[GoogleItem] = [GoogleItem(i, (thumbnail[i("img").attr("id")] if i("img").attr("id") else None)) for i in data.items()]
        self.index: int = index  # 当前页
        self.page: int = len(pages)  # 总页数
        self.pages: List[PyQuery] = pages  # 页面源

    def get_page_url(self, index: int) -> str:
        return f'https://www.google.com{self.pages[index - 1]("a").eq(0).attr("href")}'

    @staticmethod
    def create_list_thumbnail(data: PyQuery):
        d: dict = {}
        base_64_regex = compile(r"(data:image\/(?:jpeg|jpg|png|gif);base64,[^'\"]+)")
        extract_id = compile(r"(\[(?:[\"']dimg_\d+['\"],?\s*)*[\"']dimg_\d+['\"]\])")

        base64 = base_64_regex.findall(data.text())
        id = extract_id.findall(data.text())

        for index, a in enumerate(id):
            a = a.replace("[", "").replace("]", "").replace('"', '').replace("'", "")

            if "," in a:
                a = a.split(",")
                for x in a:
                    d[x] = str(base64[index]).replace("\\x3d", "=")
                continue

            d[a] = str(base64[index]).replace("\\x3d", "=")
        return d