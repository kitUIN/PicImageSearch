from pathlib import Path
from typing import Any, Dict, Optional, Union

from .model import GoogleResponse
from .network import HandOver


class Google(HandOver):
    """API client for the Google image search engine.

    Attributes:
        url: The URL endpoint for the Google API.
        params: Query parameters for the Google API.
    """

    def __init__(self, **request_kwargs: Any):
        """Initializes Google API client with configuration.

        Args:
            **request_kwargs: Additional keyword arguments for request configuration.
        """
        super().__init__(**request_kwargs)
        self.url = "https://www.google.com/searchbyimage"

    async def _navigate_page(
        self, resp: GoogleResponse, offset: int
    ) -> Optional[GoogleResponse]:
        """Navigate to the next or previous page of the search results.

        Args:
            resp: The response from the previous search.
            offset: The offset to navigate to. Negative values navigate backwards.

        Returns:
            An instance of GoogleResponse containing the search results and additional metadata.
            Or None if the offset is out of bounds.
        """

        index = resp.pages.index(resp.url)
        new_index = index + offset
        if new_index < 0 or new_index >= len(resp.pages):
            return None
        _resp = await self.get(resp.pages[new_index])
        return GoogleResponse(_resp.text, _resp.url)

    async def pre_page(self, resp: GoogleResponse) -> Optional[GoogleResponse]:
        """Navigate to the previous page of the search results.

        Args:
            resp: The response from the previous search.

        Returns:
            An instance of GoogleResponse containing the search results and additional metadata.
            Or None if there is no previous page.
        """

        return await self._navigate_page(resp, -1)

    async def next_page(self, resp: GoogleResponse) -> Optional[GoogleResponse]:
        """Navigate to the next page of the search results.

        Args:
            resp: The response from the previous search.

        Returns:
            An instance of GoogleResponse containing the search results and additional metadata.
            Or None if there is no next page.
        """
        return await self._navigate_page(resp, 1)

    async def search(
        self, url: Optional[str] = None, file: Union[str, bytes, Path, None] = None
    ) -> GoogleResponse:
        """Performs a reverse image search on Google using the URL or file of the image.

        The user must provide either a URL or a file.

        Args:
            url: URL of the image to search.
            file: Image file to search. Can be a file path (str or Path) or raw bytes.

        Returns:
            An instance of GoogleResponse containing the search results and additional metadata.

        Raises:
            ValueError: If neither `url` nor `file` is provided.
        """
        params: Dict[str, Any] = {"sbisrc": 1}
        if url:
            params["image_url"] = url
            resp = await self.get(self.url, params=params)
        elif file:
            files = {
                "encoded_image": file if isinstance(file, bytes) else open(file, "rb")
            }
            resp = await self.post(f"{self.url}/upload", data=params, files=files)
        else:
            raise ValueError("url or file is required")
        return GoogleResponse(resp.text, resp.url)
