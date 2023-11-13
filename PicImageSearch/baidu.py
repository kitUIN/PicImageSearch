import re
from json import loads as json_loads
from pathlib import Path
from typing import Any, Dict, Optional, Union

from .model import BaiDuResponse
from .network import HandOver


class BaiDu(HandOver):
    """API client for the BaiDu image search engine.

    Attributes:
        url: The URL endpoint for the BaiDu API.
        params: Query parameters for the BaiDu API.
    """

    def __init__(self, **request_kwargs: Any):
        """Initializes BaiDu API client with configuration.

        Args:
            **request_kwargs: Additional keyword arguments for request configuration.
        """
        super().__init__(**request_kwargs)

    async def search(
        self, url: Optional[str] = None, file: Union[str, bytes, Path, None] = None
    ) -> BaiDuResponse:
        """Performs a reverse image search on BaiDu using the URL or file of the image.

        The user must provide either a URL or a file.

        Args:
            url: URL of the image to search.
            file: Image file to search. Can be a file path (str or Path) or raw bytes.

        Returns:
            An instance of BaiDuResponse containing the search results and additional metadata.

        Raises:
            ValueError: If neither `url` nor `file` is provided.
        """
        params = {"from": "pc"}
        files: Optional[Dict[str, Any]] = None
        if url:
            params["image"] = url
        elif file:
            files = (
                {"image": file}
                if isinstance(file, bytes)
                else {"image": open(file, "rb")}
            )
        else:
            raise ValueError("url or file is required")
        resp = await self.post(
            "https://graph.baidu.com/upload", params=params, files=files
        )
        next_url = (json_loads(resp.text))["data"]["url"]
        resp = await self.get(next_url)
        final_url = resp.url
        next_url = (re.search(r'"firstUrl":"([^"]+)"', resp.text)[1]).replace(r"\/", "/")  # type: ignore
        resp = await self.get(next_url)
        return BaiDuResponse(json_loads(resp.text), final_url)
