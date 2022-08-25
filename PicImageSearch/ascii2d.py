from pathlib import Path
from typing import Any, Dict, Optional, Union

from .model import Ascii2DResponse
from .network import HandOver


class Ascii2D(HandOver):
    """
    Ascii2D
    -----------
    Reverse image from https://ascii2d.net\n


    Params Keys
    -----------
    :param **request_kwargs: proxies and bypass settings.\n
    :param bovw(bool): use ascii2d bovw search, default False \n
    """

    def __init__(self, bovw: bool = False, **request_kwargs: Any):
        super().__init__(**request_kwargs)
        self.bovw: bool = bovw

    async def search(
        self, url: Optional[str] = None, file: Union[str, bytes, Path, None] = None
    ) -> Ascii2DResponse:
        """
        Ascii2D
        -----------
        Reverse image from https://ascii2d.net\n


        Return Attributes
        -----------
        • .origin = Raw data from scrapper\n
        • .raw = Simplified data from scrapper\n
        • .raw[0] = First index of simplified data that was found\n
        • .raw[0].title = First index of title that was found\n
        • .raw[0].url = First index of url source that was found\n
        • .raw[0].authors = First index of authors that was found\n
        • .raw[0].thumbnail = First index of url image that was found\n
        • .raw[0].detail = First index of details image that was found
        """
        if url:
            ascii2d_url = "https://ascii2d.net/search/uri"
            resp_text, resp_url, _ = await self.post(ascii2d_url, data={"uri": url})
        elif file:
            ascii2d_url = "https://ascii2d.net/search/file"
            data: Dict[str, Any] = (
                {"file": file}
                if isinstance(file, bytes)
                else {"file": open(file, "rb")}
            )
            resp_text, resp_url, _ = await self.post(ascii2d_url, data=data)
        else:
            raise ValueError("url or file is required")

        # 如果启用bovw选项，第一次请求是向服务器提交文件
        if self.bovw:
            resp_text, resp_url, _ = await self.get(
                resp_url.replace("/color/", "/bovw/")
            )

        return Ascii2DResponse(resp_text, resp_url)
