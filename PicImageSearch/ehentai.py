from typing import Any

from loguru import logger

from .network import HandOver
from .Utils import EHentaiResponse


class EHentai(HandOver):
    def __init__(
        self,
        cover: bool = False,
        similar: bool = True,
        exp: bool = False,
        **request_kwargs: Any
    ):
        super().__init__(**request_kwargs)
        self.covers: bool = cover
        self.similar: bool = similar
        self.exp: bool = exp

    @logger.catch()
    async def search(self, file_path: str, ex: bool = False) -> EHentaiResponse:
        url = (
            "https://exhentai.org/upld/image_lookup.php"
            if ex
            else "https://upld.e-hentai.org/image_lookup.php"
        )
        data = {"f_sfile": "search"}
        files = {"sfile": open(file_path, "rb")}
        if self.covers:
            data["fs_covers"] = "on"
        if self.similar:
            data["fs_similar"] = "on"
        if self.exp:
            data["fs_exp"] = "on"
        resp = await self.post(url=url, data=data, files=files)
        logger.info(resp.headers)
        logger.info(resp.text)
        return EHentaiResponse(resp)
