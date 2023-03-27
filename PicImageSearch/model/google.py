from re import compile
from typing import Dict, List, Optional

from pyquery import PyQuery


class GoogleItem:
    def __init__(self, data: PyQuery, thumbnail: Optional[str]):
        self.origin: PyQuery = data  # 原始数据
        self.title: str = data("h3").text()
        self.url: str = data("a").eq(0).attr("href")
        self.thumbnail: Optional[str] = thumbnail


class GoogleResponse:
    def __init__(
        self,
        data: PyQuery,
        pages: List[str],
        index: int,
        script_list: List[PyQuery],
    ):
        self.origin: PyQuery = data  # 原始数据
        # 结果返回值
        thumbnail_dict: Dict[str, str] = self.create_thumbnail_dict(script_list)
        self.raw: List[GoogleItem] = [
            GoogleItem(
                i,
                (thumbnail_dict[i("img").eq(1).attr("id")] if i("img").eq(1).attr("id") else None),
            )
            for i in data.items()
        ]
        self.index: int = index  # 当前页
        self.page: int = len(pages)  # 总页数
        self.pages: List[str] = pages  # 页面源

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
