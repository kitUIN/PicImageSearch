from loguru import logger
from lxml.html import HTMLParser, fromstring
from pyquery import PyQuery

from .network import HandOver
from .Utils import Ascii2DResponse


class Ascii2D(HandOver):
    """
    Ascii2D
    -----------
    Reverse image from https://ascii2d.net\n


    Params Keys
    -----------
    :param **requests_kwargs:   proxies settings.\n
    :param bovw(boolean):   use ascii2d bovw search, default False \n
    """

    def __init__(self, bovw=False, **requests_kwargs):
        super().__init__(**requests_kwargs)
        self.requests_kwargs = requests_kwargs
        self.bovw = bovw

    @staticmethod
    def _slice(res: str) -> Ascii2DResponse:
        utf8_parser = HTMLParser(encoding="utf-8")
        d = PyQuery(fromstring(res, parser=utf8_parser))("div.row.item-box")
        return Ascii2DResponse(d)

    @logger.catch()
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
            res = await self.post(ascii2d_url, _data={"uri": url})
        else:  # 是否是本地文件
            ascii2d_url = "https://ascii2d.net/search/file"
            res = await self.post(ascii2d_url, _files={"file": open(url, "rb")})

        # 如果启用bovw选项，第一次请求是向服务器提交文件
        if self.bovw:
            res = await self.get(str(res.url).replace("/color/", "/bovw/"))

        return self._slice(res.text)
