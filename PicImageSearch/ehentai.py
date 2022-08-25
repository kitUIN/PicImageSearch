import io
from pathlib import Path
from typing import Any, Dict, Optional, Union

from .model import EHentaiResponse
from .network import HandOver


class EHentai(HandOver):
    def __init__(
        self,
        covers: bool = False,
        similar: bool = True,
        exp: bool = False,
        **request_kwargs: Any
    ):
        super().__init__(**request_kwargs)
        self.covers: bool = covers
        self.similar: bool = similar
        self.exp: bool = exp

    async def search(
        self,
        url: Optional[str] = None,
        file: Union[str, bytes, Path, None] = None,
        ex: bool = False,
    ) -> EHentaiResponse:
        _url = (
            "https://exhentai.org/upld/image_lookup.php"
            if ex
            else "https://upld.e-hentai.org/image_lookup.php"
        )
        data: Dict[str, Any] = {"f_sfile": "search"}
        if url:
            data["sfile"] = io.BytesIO(await self.download(url))
        elif file:
            data["sfile"] = file if isinstance(file, bytes) else open(file, "rb")
        else:
            raise ValueError("url or file is required")
        if self.covers:
            data["fs_covers"] = "on"
        if self.similar:
            data["fs_similar"] = "on"
        if self.exp:
            data["fs_exp"] = "on"
        resp_text, resp_url, _ = await self.post(url=_url, data=data)
        return EHentaiResponse(resp_text, resp_url)
