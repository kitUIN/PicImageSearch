from typing import Any, BinaryIO, Optional

from lxml.html import HTMLParser, fromstring
from pyquery import PyQuery

from .model import IqdbResponse
from .network import HandOver


class Iqdb(HandOver):
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
        if url:
            data = {"url": url}
            if force_gray:  # 忽略颜色
                data["forcegray"] = "on"
            resp = await self.post(iqdb_url, data=data)
        elif file:
            data = {"forcegray": "on"} if force_gray else None  # type: ignore
            resp = await self.post(iqdb_url, data=data, files={"file": file})
        else:
            raise ValueError("url or file is required")
        return self._slice(resp.text)
