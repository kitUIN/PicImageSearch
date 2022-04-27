from typing import Any, BinaryIO, Optional

from .model import BaiDuResponse
from .network import HandOver


class BaiDu(HandOver):
    def __init__(self, **request_kwargs: Any):
        super().__init__(**request_kwargs)

    async def search(
        self, url: Optional[str] = None, file: Optional[BinaryIO] = None
    ) -> BaiDuResponse:
        params = {"from": "pc"}
        files = None
        if url:
            params["image"] = url
        elif file:
            files = {"image": file}
        else:
            raise ValueError("url or file is required")
        resp = await self.post(
            "https://graph.baidu.com/upload", params=params, files=files
        )
        resp = await self.get(resp.json()["data"]["url"])
        return BaiDuResponse(resp)
