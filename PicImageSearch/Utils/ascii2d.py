from typing import Dict, List

from pyquery import PyQuery


class Ascii2DItem:
    def __init__(self, data: PyQuery):
        self.origin: PyQuery = data  # 原始数据
        info = self._get_info(data("div.detail-box.gray-link"))
        # 原图长宽，类型，大小
        self.detail: str = data("small").eq(0).text()
        self.thumbnail: str = "https://ascii2d.net" + data("img").eq(0).attr("src")
        self.url: str = info["url"]
        self.title: str = info["title"]
        self.author: str = info["author"]
        self.author_url: str = info["author_url"]
        self.mark: str = info["mark"]

    @staticmethod
    def _get_info(data: PyQuery) -> Dict[str, str]:
        info = {
            "url": "",
            "title": "",
            "author_url": "",
            "author": "",
            "mark": "",
        }

        infos = data.find("h6")
        if infos:
            links = infos.find("a")
            if links:
                info["url"] = links.eq(0).attr("href")
                info["mark"] = infos("small").eq(0).text()
                if len(list(links.items())) > 1:
                    info["title"] = links.eq(0).text()
                    info["author_url"] = links.eq(1).attr("href")
                    info["author"] = links.eq(1).text()
                elif links.eq(0).parents("small"):
                    info["title"] = infos.contents().eq(0).text()

        return info


class Ascii2DResponse:
    def __init__(self, data: PyQuery):
        self.origin: PyQuery = data  # 原始数据
        # 结果返回值
        self.raw: List[Ascii2DItem] = [Ascii2DItem(i) for i in data.items()]
