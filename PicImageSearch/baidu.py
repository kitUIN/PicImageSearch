from json import loads as json_loads
from typing import Any, BinaryIO, Optional

from aiohttp import FormData

from .model import BaiDuResponse
from .network import HandOver


class BaiDu(HandOver):
    def __init__(self, **request_kwargs: Any):
        super().__init__(**request_kwargs)

    async def search(
        self, url: Optional[str] = None, file: Optional[BinaryIO] = None
    ) -> BaiDuResponse:
        params = {"from": "pc"}
        data = None
        if url:
            params["image"] = url
        elif file:
            data = FormData()
            data.add_field("image", file, filename="file.png")
        else:
            raise ValueError("url or file is required")
        resp_text, resp_url, _ = await self.post(
            "https://graph.baidu.com/upload", params=params, data=data
        )
        resp_text, resp_url, _ = await self.get((json_loads(resp_text))["data"]["url"])
        return BaiDuResponse(resp_text, resp_url)
