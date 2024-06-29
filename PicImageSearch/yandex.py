from pathlib import Path
from typing import Any, Optional, Union

from .model import YandexResponse
from .network import HandOver
from .utils import read_file


class Yandex(HandOver):
    """API client for the Yandex image search engine.

    Used for performing reverse image searches using Yandex service.

    Attributes:
        base_url: The base URL for Yandex searches.
    """

    def __init__(
        self,
        base_url: str = "https://yandex.com",
        **request_kwargs: Any,
    ):
        """Initializes a Yandex API client with specified configurations.

        Args:
            base_url: The base URL for Yandex searches.
            **request_kwargs: Additional arguments for network requests.
        """
        super().__init__(**request_kwargs)
        self.base_url = f"{base_url}/images/search"

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
        params = {"rpt": "imageview", "cbir_page": "sites"}
        if url:
            params["url"] = url
            resp = await self.get(self.base_url, params=params)
        elif file:
            files = {"upfile": read_file(file)}
            resp = await self.post(
                self.base_url, params=params, data={"prg": 1}, files=files
            )
        else:
            raise ValueError("Either 'url' or 'file' must be provided")

        return YandexResponse(resp.text, resp.url)
