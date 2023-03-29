from pathlib import Path
from typing import Any, Dict, Optional, Union

from .model import GoogleResponse
from .network import HandOver


class Google(HandOver):
    """
    Google
    -----------
    Reverse image from https://www.google.com\n


    Params Keys
    -----------
    :param **request_kwargs: proxies settings
    """

    def __init__(self, **request_kwargs: Any):
        super().__init__(**request_kwargs)
        self.url = "https://www.google.com/searchbyimage"

    async def pre_page(self, resp: GoogleResponse) -> Optional[GoogleResponse]:
        index = resp.pages.index(resp.url)
        if index == 0:
            return None
        resp_text, resp_url, _ = await self.get(resp.pages[index - 1])
        return GoogleResponse(resp_text, resp_url)

    async def next_page(self, resp: GoogleResponse) -> Optional[GoogleResponse]:
        index = resp.pages.index(resp.url)
        if index == len(resp.pages) - 1:
            return None
        resp_text, resp_url, _ = await self.get(resp.pages[index + 1])
        return GoogleResponse(resp_text, resp_url)

    async def search(
        self, url: Optional[str] = None, file: Union[str, bytes, Path, None] = None
    ) -> GoogleResponse:
        """
        Google
        -----------
        Reverse image from https://www.google.com\n


        Return Attributes
        -----------
        • .origin = Raw data from scrapper\n
        • .raw = Simplified data from scrapper\n
        • .raw[2] = Third index of simplified data that was found <Should start from index 2,
                    because from there is matching image>\n
        • .raw[2].title = Third index of title that was found\n
        • .raw[2].url = Third index of url source that was found\n
        • .raw[2].thumbnail = Third index of base64 string image that was found
        """
        params: Dict[str, Any] = {"sbisrc": 1}
        if url:
            params["image_url"] = url
            resp_text, resp_url, _ = await self.get(self.url, params=params)
        elif file:
            files = {
                "encoded_image": file if isinstance(file, bytes) else open(file, "rb")
            }
            resp_text, resp_url, _ = await self.post(
                f"{self.url}/upload", data=params, files=files
            )
        else:
            raise ValueError("url or file is required")
        return GoogleResponse(resp_text, resp_url)
