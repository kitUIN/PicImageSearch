from pathlib import Path
from typing import Any, Dict, Optional, Union

from .model import IqdbResponse
from .network import HandOver


class Iqdb(HandOver):
    """
    Iqdb
    -----------
    Reverse image from https://iqdb.org\n


    Params Keys
    -----------
    :param **request_kwargs: proxies setting.\n
    """

    def __init__(self, **request_kwargs: Any):
        super().__init__(**request_kwargs)

    async def search(
        self,
        url: Optional[str] = None,
        file: Union[str, bytes, Path, None] = None,
        force_gray: bool = False,
        is_3d: bool = False,
    ) -> IqdbResponse:
        iqdb_url = "https://3d.iqdb.org/" if is_3d else "https://iqdb.org/"
        data: Dict[str, Any] = {}
        if force_gray:  # 忽略颜色
            data["forcegray"] = "on"
        if url:
            data["url"] = url
            resp = await self.post(iqdb_url, data=data)
        elif file:
            files = {"file": file if isinstance(file, bytes) else open(file, "rb")}
            resp = await self.post(iqdb_url, data=data, files=files)
        else:
            raise ValueError("url or file is required")
        return IqdbResponse(resp.text)
