from typing import Any, BinaryIO, Optional

from aiohttp import FormData
from lxml.html import HTMLParser, fromstring
from pyquery import PyQuery

from .model import IqdbResponse
from .network import HandOver


class Iqdb(HandOver):
    """
    Iqdb
    -----------
    Reverse image from https://iqdb.org\n


    Params Keys
    -----------
    :param **request_kwargs: proxies and bypass settings.\n
    """

    def __init__(self, **request_kwargs: Any):
        super().__init__(**request_kwargs)

    @staticmethod
    def _slice(resp: str) -> IqdbResponse:
        utf8_parser = HTMLParser(encoding="utf-8")
        d = PyQuery(fromstring(resp, parser=utf8_parser))
        return IqdbResponse(d)

    async def search(
        self,
        url: Optional[str] = None,
        file: Optional[BinaryIO] = None,
        force_gray: bool = False,
        is_3d: bool = False,
    ) -> IqdbResponse:
        iqdb_url = "https://3d.iqdb.org/" if is_3d else "https://iqdb.org/"
        data = FormData()
        if force_gray:  # 忽略颜色
            data.add_field("forcegray", "on")
        if url:
            data.add_field("url", url)
            resp_text, _, _ = await self.post(iqdb_url, data=data)
        elif file:
            data.add_field("file", file, filename="file.png")
            resp_text, _, _ = await self.post(iqdb_url, data=data)
        else:
            raise ValueError("url or file is required")
        return self._slice(resp_text)
