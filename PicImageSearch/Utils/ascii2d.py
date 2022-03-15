from typing import List


class Ascii2DNorm:
    ascii2d_url = "https://ascii2d.net"

    def __init__(self, data):
        self.thumbnail: str = ""
        """缩略图地址"""
        self.detail: str = data[3].small.string
        """原图长宽，类型，大小"""
        self.title: str = ""
        """标题"""
        self.authors: str = ""
        """作者"""
        self.url: str = ""
        """url地址"""
        self.marks: str = ""

        self._arrange(data)

    def _arrange(self, data):
        o_url = data[3].find("div", class_="detail-box gray-link").contents
        urls = self._get_urls(o_url)
        self.thumbnail = self.ascii2d_url + data[1].find("img")["src"]
        self.url = urls["url"]
        self.title = urls["title"]
        self.authors = urls["authors"]
        self.marks = urls["mark"]

    @staticmethod
    def _get_urls(data):
        all_urls = {
            "url": "",
            "title": "",
            "authors_urls": "",
            "authors": "",
            "mark": "",
        }

        for x in data:
            if x == "\n":
                continue
            try:
                origin = x.find_all("a")
                all_urls["url"] = origin[0]["href"]
                all_urls["title"] = origin[0].string
                all_urls["authors_urls"] = origin[1]["href"]
                all_urls["authors"] = origin[1].string
                all_urls["mark"] = x.small.string
            except:
                pass
        return all_urls

    def __repr__(self):
        return f"<NormAscii2D(title={repr(self.title)}, authors={self.authors}, mark={self.marks})>"


class Ascii2DResponse:
    def __init__(self, res):
        self.origin: list = res
        """原始返回值"""
        self.raw: List[Ascii2DNorm] = list()
        """结果返回值"""
        for ele in self.origin:
            detail = ele.contents
            self.raw.append(Ascii2DNorm(detail))

    def __repr__(self):
        return f"<Ascii2DResponse(count={repr(len(self.origin))}>"
