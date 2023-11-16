from pathlib import Path
from typing import Any, Dict, Optional, Union

from .model import YandexResponse
from .network import HandOver


class Yandex(HandOver):
    """API client for the Yandex image search engine.

    Used for performing reverse image searches using Yandex service.

    Attributes:
        url: The base URL for Yandex search.
    """

    def __init__(self, **request_kwargs: Any):
        """Initializes a Yandex API client with specified configurations.

        Args:
            **request_kwargs: Additional arguments for network requests.
        """
        super().__init__(**request_kwargs)
        self.url = "https://yandex.com/images/search"

    async def search(
        self, url: Optional[str] = None, file: Union[str, bytes, Path, None] = None
    ) -> YandexResponse:
        """Performs a reverse image search on Yandex.

        Supports searching by image URL or by uploading an image file.

        Requires either 'url' or 'file' to be provided.

        Args:
            url: URL of the image to search.
            file: Local image file (path or bytes) to search.

        Returns:
            YandexResponse: Contains search results and additional information.

        Raises:
            ValueError: If neither 'url' nor 'file' is provided.
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
            raise ValueError("Either 'url' or 'file' must be provided")

        return YandexResponse(resp.text, resp.url)
