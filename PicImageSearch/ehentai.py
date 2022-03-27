import io
from typing import Any

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

    async def search(self, url: str, ex: bool = False) -> EHentaiResponse:
        _url = (
            "https://exhentai.org/upld/image_lookup.php"
            if ex
            else "https://upld.e-hentai.org/image_lookup.php"
        )
        data = {"f_sfile": "search"}
        if url[:4] == "http":  # 网络url
            file_content = io.BytesIO((await self.get(url)).content)
            files = {"sfile": file_content}
        else:  # 本地文件
            files = {"sfile": open(url, "rb")}  # type: ignore
        if self.covers:
            data["fs_covers"] = "on"
        if self.similar:
            data["fs_similar"] = "on"
        if self.exp:
            data["fs_exp"] = "on"
        resp = await self.post(url=_url, data=data, files=files)
        return EHentaiResponse(resp)
