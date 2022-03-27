from typing import Any

from .model import BaiDuResponse
from .network import HandOver


class BaiDu(HandOver):
    def __init__(self, **request_kwargs: Any):
        super().__init__(**request_kwargs)

    async def search(self, url: str) -> BaiDuResponse:
        params = {"from": "pc"}
        files = None
        if url[:4] == "http":  # 网络url
            params["image"] = url
        else:
            # 上传文件
            files = {"image": open(url, "rb")}
        resp = await self.post(
            "https://graph.baidu.com/upload", params=params, files=files
        )
        resp = await self.get(resp.json()["data"]["url"])
        return BaiDuResponse(resp)
