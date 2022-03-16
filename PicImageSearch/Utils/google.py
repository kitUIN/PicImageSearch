import re
from typing import List


class GoogleNorm:
    def __init__(self, data):
        self.thumbnail: str = ""
        """缩略图地址"""
        self.title: str = ""
        """标题"""
        self.url: str = ""
        """url地址"""
        self._arrange(data)

    def _arrange(self, data):
        get_data = self._get_data(data)
        self.title = get_data["title"]
        self.url = get_data["url"]
        self.thumbnail = get_data["thumbnail"]

    def _get_data(self, datas):

        data = {
            "thumbnail": "",
            "title": "",
            "url": "",
        }

        for x in datas:
            try:
                origin = x.find_all("h3")
                data["title"] = origin[0].string
                url = x.find_all("a")
                data["url"] = url[0]["href"]
                img = self._get_thumbnail(url)
                data["thumbnail"] = img
            except:
                pass

        return data

    @staticmethod
    def _get_thumbnail(data):
        google_url = "https://www.google.com/"
        regex = re.compile(
            r"((http(s)?(://))+(www\.)?([\w\-./])*(\.[a-zA-Z]{2,3}/?))[^\s\b\n|]*[^.,;:?!@^$ -]"
        )

        thumbnail = "No detectable url"

        for a in range(5):
            try:
                if re.findall("jpg|png", regex.search(data[a]["href"]).group(1)):
                    thumbnail = regex.search(data[a]["href"]).group(1)
                elif re.findall("/imgres", data[a]["href"]):
                    thumbnail = f"{google_url}{data[a]['href']}"
            except:
                continue

        return thumbnail

    def __repr__(self):
        return f"<NormGoogle(title={repr(self.title)}, url={self.url}, thumbnail={self.thumbnail})>"


class GoogleResponse:
    def __init__(self, res, pages, index):
        self.origin: list = res
        """原始返回值"""
        self.raw: List[GoogleNorm] = list()
        """结果返回值"""
        self.index: int = index
        """当前页"""
        self.page: int = len(pages)
        """总页数"""
        self.pages: list = pages
        """页面源"""

        for ele in self.origin:
            detail = ele.contents
            self.raw.append(GoogleNorm(detail))

    def get_page_url(self, index):
        if self.index != index:
            url = "https://www.google.com" + self.pages[index - 1].a["href"]
            print(url)
            return url

    def __repr__(self):
        return f"<GoogleResponse(count{repr(len(self.origin))})>"
