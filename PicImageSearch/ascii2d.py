from typing import Any

from lxml.html import HTMLParser, fromstring
from pyquery import PyQuery

from .model import Ascii2DResponse
from .network import HandOver


class Ascii2D(HandOver):
    """
    Ascii2D
    -----------
    Reverse image from https://ascii2d.net\n


    Params Keys
    -----------
    :param **request_kwargs:   proxies settings.\n
    :param bovw(boolean):   use ascii2d bovw search, default False \n
    """

    def __init__(self, bovw: bool = False, **request_kwargs: Any):
        super().__init__(**request_kwargs)
        self.bovw: bool = bovw

    @staticmethod
    def _slice(resp: str) -> Ascii2DResponse:
        utf8_parser = HTMLParser(encoding="utf-8")
        d = PyQuery(fromstring(resp, parser=utf8_parser))("div.row.item-box")
        return Ascii2DResponse(d)

    async def search(self, url: str) -> Ascii2DResponse:
        """
        Ascii2D
        -----------
        Reverse image from https://ascii2d.net\n


        Return Attributes
        -----------
        • .origin = Raw data from scrapper\n
        • .raw = Simplified data from scrapper\n
        • .raw[0] = First index of simplified data that was found\n
        • .raw[0].title = First index of title that was found\n
        • .raw[0].url = First index of url source that was found\n
        • .raw[0].authors = First index of authors that was found\n
        • .raw[0].thumbnail = First index of url image that was found\n
        • .raw[0].detail = First index of details image that was found
        """
        if url[:4] == "http":  # 网络url
            ascii2d_url = "https://ascii2d.net/search/uri"
            resp = await self.post(ascii2d_url, data={"uri": url})
        else:  # 本地文件
            ascii2d_url = "https://ascii2d.net/search/file"
            resp = await self.post(ascii2d_url, files={"file": open(url, "rb")})

        # 如果启用bovw选项，第一次请求是向服务器提交文件
        if self.bovw:
            resp = await self.get(str(resp.url).replace("/color/", "/bovw/"))

        return self._slice(resp.text)
