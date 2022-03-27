from typing import Any
from urllib.parse import quote

from lxml.html import HTMLParser, fromstring
from pyquery import PyQuery

from .model import GoogleResponse
from .network import HandOver


class Google(HandOver):
    """
    Google
    -----------
    Reverse image from https://www.google.com\n


    Params Keys
    -----------
    :param **request_kwargs: proxies settings
    """

    def __init__(self, **request_kwargs: Any):
        super().__init__(**request_kwargs)
        self.url = "https://www.google.com/searchbyimage"

    @staticmethod
    def _slice(resp: str, index: int = 1) -> GoogleResponse:
        utf8_parser = HTMLParser(encoding="utf-8")
        d = PyQuery(fromstring(resp, parser=utf8_parser))
        data = d.find(".g")
        pages = list(d.find("td").items())[1:-1]
        return GoogleResponse(data, pages, index)

    async def goto_page(self, url: str, index: int) -> GoogleResponse:
        resp = await self.get(url)
        return self._slice(resp.text, index)

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
        if url[:4] == "http":
            encoded_image_url = quote(url, safe="")
            params = {"image_url": encoded_image_url}
            resp = await self.get(self.url, params=params)
        else:
            files = {"encoded_image": (url, open(url, "rb"))}
            resp = await self.post(f"{self.url}/upload", files=files)
        return self._slice(resp.text, 1)
