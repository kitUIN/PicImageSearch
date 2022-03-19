from urllib.parse import quote

from loguru import logger
from lxml.html import HTMLParser, fromstring
from pyquery import PyQuery

from .network import HandOver
from .Utils import GoogleResponse


class Google(HandOver):
    """
    Google
    -----------
    Reverse image from https://www.google.com\n


    Params Keys
    -----------
    :param **requests_kwargs: proxies settings
    """

    def __init__(self, **request_kwargs):
        super().__init__(**request_kwargs)
        self.url = "https://www.google.com/searchbyimage"
        self.params = {}
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0",
        }
        self.requests_kwargs = request_kwargs

    @staticmethod
    def _slice(res: str, index: int = 1) -> GoogleResponse:
        utf8_parser = HTMLParser(encoding="utf-8")
        d = PyQuery(fromstring(res, parser=utf8_parser))
        data = d.find(".g")
        pages = list(d.find("td").items())[1:-1]
        return GoogleResponse(data, pages, index)

    async def goto_page(self, url: str, index: int) -> GoogleResponse:
        if url:
            response = await self.get(url, _headers=self.header)
            return self._slice(response.text, index)

    @logger.catch()
    async def search(self, url: str) -> GoogleResponse:
        """
        Google
        -----------
        Reverse image from https://www.google.com\n


        Return Attributes
        -----------
        • .origin = Raw data from scrapper\n
        • .raw = Simplified data from scrapper\n
        • .raw[2] = Second index of simplified data that was found <Should start from index 2, because from there is matching image>\n
        • .raw[2].title = First index of title that was found\n
        • .raw[2].url = First index of url source that was found\n
        • .raw[2].thumbnail = First index of url image that was found
        """
        params = self.params
        if url[:4] == "http":
            encoded_image_url = quote(url, safe="")
            params["image_url"] = encoded_image_url
            response = await self.get(self.url, _params=params, _headers=self.header)
        else:
            multipart = {"encoded_image": (url, open(url, "rb"))}
            response = await self.post(
                f"{self.url}/upload", _files=multipart, _headers=self.header
            )
        return self._slice(response.text, 1)
