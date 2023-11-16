import re
from json import loads as json_loads
from pathlib import Path
from typing import Any, Dict, Optional, Union

from .model import BaiDuResponse
from .network import HandOver


class BaiDu(HandOver):
    """API client for the BaiDu image search engine.

    Used for performing reverse image searches using BaiDu service.
    """

    def __init__(self, **request_kwargs: Any):
        """Initializes a BaiDu API client with specified configurations.

        Args:
            **request_kwargs: Additional arguments for network requests.
        """
        super().__init__(**request_kwargs)

    async def search(
        self, url: Optional[str] = None, file: Union[str, bytes, Path, None] = None
    ) -> BaiDuResponse:
        """Performs a reverse image search on BaiDu.

        Supports searching by image URL or by uploading an image file.

        Requires either 'url' or 'file' to be provided.

        Args:
            url: URL of the image to search.
            file: Local image file (path or bytes) to search.

        Returns:
            BaiDuResponse: Contains search results and additional information.

        Raises:
            ValueError: If neither 'url' nor 'file' is provided.

        Note:
            The search process involves multiple HTTP requests to BaiDu's API.
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
            raise ValueError("Either 'url' or 'file' must be provided")

        resp = await self.post(
            "https://graph.baidu.com/upload", params=params, files=files
        )
        next_url = (json_loads(resp.text))["data"]["url"]
        resp = await self.get(next_url)
        final_url = resp.url
        next_url = (re.search(r'"firstUrl":"([^"]+)"', resp.text)[1]).replace(r"\/", "/")  # type: ignore
        resp = await self.get(next_url)
        return BaiDuResponse(json_loads(resp.text), final_url)
