from typing import Any

from loguru import logger
from lxml.html import HTMLParser, fromstring
from pyquery import PyQuery

from .network import HandOver
from .Utils import IqdbResponse


class Iqdb(HandOver):
    """
    Iqdb and Iqdb 3d
    -----------
    Reverse image from https://iqdb.org\n


    Params Keys
    -----------
    :param **request_kwargs: proxies settings
    """

    def __init__(self, **request_kwargs: Any):
        super().__init__(**request_kwargs)
        self.url = "https://iqdb.org/"
        self.url_3d = "https://3d.iqdb.org/"

    @staticmethod
    def _slice(resp: str) -> IqdbResponse:
        utf8_parser = HTMLParser(encoding="utf-8")
        d = PyQuery(fromstring(resp, parser=utf8_parser))
        return IqdbResponse(d)

    # TODO: &forcegray=on
    @logger.catch()
    async def search(self, url: str) -> IqdbResponse:
        """
        Iqdb
        -----------
        Reverse image from https://iqdb.org\n


        Return Attributes
        -----------
        • .origin = Raw data from scrapper\n
        • .raw = Simplified data from scrapper\n
        • .saucenao = e.g.  https://saucenao.com/search.php?db=999&dbmaski=32768&url=https://iqdb.org/thu/thu_ccb14a40.jpg
        • .ascii2d = e.g.  https://ascii2d.net/search/url/https://iqdb.org/thu/thu_ccb14a40.jpg
        • .tineye = e.g.  https://tineye.com/search?url=https://iqdb.org/thu/thu_ccb14a40.jpg
        • .google = e.g.   https://www.google.com/searchbyimage?image_url=https://iqdb.org/thu/thu_ccb14a40.jpg&safe=off
        • .more = other (low similarity) Simplified data from scrapper\n
        • .raw[0].content = First index of content <Index 0 `Best match` or Index 1 etc `Additional match`>\n
        • .raw[0].source = First index of source website that was found\n
        • .raw[0].other_source = other index of source website that was found\n
        • .raw[0].url = First index of url source that was found\n
        • .raw[0].thumbnail = First index of url image that was found\n
        • .raw[0].similarity = First index of similarity image that was found\n
        • .raw[0].size = First index detail of image size that was found

        """
        if url[:4] == "http":  # 网络url
            data = {"url": url}
            resp = await self.post(self.url, data=data)
        else:  # 是否是本地文件
            resp = await self.post(self.url, files={"file": open(url, "rb")})
        return self._slice(resp.text)

    @logger.catch()
    async def search_3d(self, url: str) -> IqdbResponse:
        """
        Iqdb 3D
        -----------
        Reverse image from https://3d.iqdb.org\n


        Return Attributes
        -----------
        • .origin = Raw data from scrapper\n
        • .raw = Simplified data from scrapper\n
        • .raw[0].content = First index of content <Index 0 `Best match` or Index 1 etc. `Additional match`>\n
        • .raw[0].title = First index of title that was found\n
        • .raw[0].url = First index of url source that was found\n
        • .raw[0].thumbnail = First index of url image that was found\n
        • .raw[0].similarity = First index of similarity image that was found\n
        • .raw[0].size = First index detail of image size that was found
        """
        if url[:4] == "http":  # 网络url
            data = {"url": url}
            resp = await self.post(self.url_3d, data=data)
        else:  # 是否是本地文件
            resp = await self.post(self.url_3d, files={"file": open(url, "rb")})
        return self._slice(resp.text)
