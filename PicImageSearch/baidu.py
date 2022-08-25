from json import loads as json_loads
from pathlib import Path
from typing import Any, Dict, Optional, Union

from .model import BaiDuResponse
from .network import HandOver


class BaiDu(HandOver):
    def __init__(self, **request_kwargs: Any):
        super().__init__(**request_kwargs)

    async def search(
        self, url: Optional[str] = None, file: Union[str, bytes, Path, None] = None
    ) -> BaiDuResponse:
        params = {"from": "pc"}
        data: Optional[Dict[str, Any]] = None
        if url:
            params["image"] = url
        elif file:
            data = (
                {"image": file}
                if isinstance(file, bytes)
                else {"image": open(file, "rb")}
            )
        else:
            raise ValueError("url or file is required")
        resp_text, resp_url, _ = await self.post(
            "https://graph.baidu.com/upload", params=params, data=data
        )
        resp_text, resp_url, _ = await self.get((json_loads(resp_text))["data"]["url"])
        return BaiDuResponse(resp_text, resp_url)
