from typing import Any

from .network import HandOver
from .Utils import BaiDuResponse


class BaiDu(HandOver):
    def __init__(self, **requests_kwargs: Any):
        super().__init__(**requests_kwargs)

    async def search(self, url: str) -> BaiDuResponse:
        params = {"from": "pc"}
        files = None
        if url[:4] == "http":  # 网络url
            params["image"] = url
        else:
            # 上传文件
            files = {"image": open(url, "rb")}
        res = await self.post(
            "https://graph.baidu.com/upload", _params=params, _files=files
        )
        res = await self.get(res.json()["data"]["url"])
        return BaiDuResponse(res)
