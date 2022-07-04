import io
from typing import Any, BinaryIO, Optional

from aiohttp import FormData

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
        file: Optional[BinaryIO] = None,
        ex: bool = False,
    ) -> EHentaiResponse:
        _url = (
            "https://exhentai.org/upld/image_lookup.php"
            if ex
            else "https://upld.e-hentai.org/image_lookup.php"
        )
        data = FormData({"f_sfile": "search"})
        if url:
            file = io.BytesIO(await self.download(url))
        if file:
            data.add_field("sfile", file, filename="file.png")
        else:
            raise ValueError("url or file is required")
        if self.covers:
            data.add_field("fs_covers", "on")
        if self.similar:
            data.add_field("fs_similar", "on")
        if self.exp:
            data.add_field("fs_exp", "on")
        resp_text, resp_url, _ = await self.post(url=_url, data=data)
        return EHentaiResponse(resp_text, resp_url)
