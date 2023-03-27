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
    def _slice(resp_text: str, resp_url: str, index: int = 1) -> GoogleResponse:
        utf8_parser = HTMLParser(encoding="utf-8")
        d = PyQuery(fromstring(resp_text, parser=utf8_parser))
        data = d.find(".g")
        pages = [f'https://www.google.com{i.attr("href")}' for i in d.find('a[aria-label~="Page"]').items()]
        pages.insert(index-1, resp_url)
        script_list = list(d.find("script").items())
        return GoogleResponse(data, pages, index, script_list)

    async def goto_page(self, resp: GoogleResponse, index: int) -> GoogleResponse:
        if index == resp.index:
            return resp
        resp_text, resp_url, _ = await self.get(resp.pages[index - 1])
        return self._slice(resp_text, resp_url, index)

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
        • .raw[2] = Third index of simplified data that was found <Should start from index 2,
                    because from there is matching image>\n
        • .raw[2].title = Third index of title that was found\n
        • .raw[2].url = Third index of url source that was found\n
        • .raw[2].thumbnail = Third index of base64 string image that was found
        """
        if url:
            file = await self.download(url)

        if not file:
            raise ValueError("url or file is required")

        data: Dict[str, Any] = (
            {"encoded_image": file}
            if isinstance(file, bytes)
            else {"encoded_image": open(file, "rb")}
        )
        resp_text, resp_url, _ = await self.post(f"{self.url}/upload", data=data)
        return self._slice(resp_text, resp_url)
