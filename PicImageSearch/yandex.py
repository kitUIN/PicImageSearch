from pathlib import Path
from typing import Any, Dict, Optional, Union

from .model import YandexResponse
from .network import HandOver


class Yandex(HandOver):
    """
    Yandex
    -----------
    Reverse image from https://yandex.com/images/search\n


    Params Keys
    -----------
    :param **request_kwargs: proxies setting.\n
    """

    def __init__(self, **request_kwargs: Any):
        super().__init__(**request_kwargs)
        self.url = "https://yandex.com/images/search"

    async def search(
        self, url: Optional[str] = None, file: Union[str, bytes, Path, None] = None
    ) -> YandexResponse:
        """
        Yandex
        -----------
        Reverse image from https://yandex.com/images/search\n


        Return Attributes
        -----------
        • .origin = Raw data from scrapper\n
        • .raw = Simplified data from scrapper\n
        • .raw[0] = First index of simplified data that was found\n
        • .raw[0].title = First index of title that was found\n
        • .raw[0].url = First index of url source that was found\n
        • .raw[0].thumbnail = First index of url image that was found\n
        • .raw[0].source = First index of source that was found\n
        • .raw[0].content = First index of content that was found\n
        • .raw[0].size = First index of size that was found\n
        """

        params = {"rpt": "imageview"}
        if url:
            params["url"] = url
            resp = await self.get(self.url, params=params)
        elif file:
            files: Dict[str, Any] = {
                "upfile": file if isinstance(file, bytes) else open(file, "rb")
            }
            resp = await self.post(
                self.url, params=params, data={"prg": 1}, files=files
            )
        else:
            raise ValueError("url or file is required")

        return YandexResponse(resp.text, resp.url)
