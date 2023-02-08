from pathlib import Path
from typing import Any, Dict, Optional, Union

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

        images_data = d.find("script")
        data = d.find(".g")
        pages = list(d.find("td").items())[1:-1]
        return GoogleResponse(data, pages, index, images_data)

    async def goto_page(self, url: str, index: int) -> GoogleResponse:
        resp_text, _, _ = await self.get(url)
        return self._slice(resp_text, index)

    async def search(
        self, url: Optional[str] = None, file: Union[str, bytes, Path, None] = None
    ) -> GoogleResponse:
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
        • .raw[2].thumbnail = First index of base64 string image that was found
        """
        if url:
            file = await self.download(url)

        if not url or not file:
            raise ValueError("url or file is required")

        data: Dict[str, Any] = (
            {"encoded_image": file}
            if isinstance(file, bytes)
            else {"encoded_image": open(file, "rb")}
        )
        resp_text, _, _ = await self.post(f"{self.url}/upload", data=data)
        return self._slice(resp_text, 1)
