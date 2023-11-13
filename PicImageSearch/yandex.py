from pathlib import Path
from typing import Any, Dict, Optional, Union

from .model import YandexResponse
from .network import HandOver


class Yandex(HandOver):
    """API client for the Yandex image search engine.

    Attributes:
        url: The URL endpoint for the Yandex API.
        params: Query parameters for the Yandex API.
    """

    def __init__(self, **request_kwargs: Any):
        """Initializes Yandex API client with configuration.

        Args:
            **request_kwargs: Additional keyword arguments for request configuration.
        """

        super().__init__(**request_kwargs)
        self.url = "https://yandex.com/images/search"

    async def search(
        self, url: Optional[str] = None, file: Union[str, bytes, Path, None] = None
    ) -> YandexResponse:
        """Performs a reverse image search on Yandex using the URL or file of the image.

        The user must provide either a URL or a file.

        Args:
            url: URL of the image to search.
            file: Image file to search. Can be a file path (str or Path) or raw bytes.

        Returns:
            An instance of YandexResponse containing the search results and additional metadata.

        Raises:
            ValueError: If neither `url` nor `file` is provided.
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
