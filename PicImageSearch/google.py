from pathlib import Path
from typing import Any, Optional, Union

from .model import GoogleResponse
from .network import HandOver
from .utils import read_file


class Google(HandOver):
    """API client for the Google image search engine.

    Used for performing reverse image searches using Google service.

    Attributes:
         base_url: The base URL for Google searches, configurable for different regions.
            Example: `https://www.google.co.jp` for searches in Japan.
    """

    def __init__(
        self,
        base_url: str = "https://www.google.com",
        **request_kwargs: Any,
    ):
        """Initializes a Google API client with specified configurations.

        Args:
            base_url: The base URL for Google searches, defaults to the international version.
            **request_kwargs: Additional arguments for network requests.
        """
        super().__init__(**request_kwargs)
        self.base_url = f"{base_url}/searchbyimage"

    async def _navigate_page(
        self, resp: GoogleResponse, offset: int
    ) -> Optional[GoogleResponse]:
        """Navigates to a specific page in search results based on the given offset.

        Args:
            resp: The current GoogleResponse instance.
            offset: Integer for page navigation, positive for forward and negative for backward.

        Returns:
            GoogleResponse: Updated response after navigating to the specified page, or None if out of range.
        """
        index = resp.pages.index(resp.url)
        new_index = index + offset
        if new_index < 0 or new_index >= len(resp.pages):
            return None
        _resp = await self.get(resp.pages[new_index])
        return GoogleResponse(_resp.text, _resp.url)

    async def pre_page(self, resp: GoogleResponse) -> Optional[GoogleResponse]:
        """Navigates to the previous page in Google search results.

        Args:
            resp: The current GoogleResponse instance.

        Returns:
            GoogleResponse: Updated response after navigating to the previous page, or None if out of range.
        """
        return await self._navigate_page(resp, -1)

    async def next_page(self, resp: GoogleResponse) -> Optional[GoogleResponse]:
        """Navigates to the next page in Google search results.

        Args:
            resp: The current GoogleResponse instance.

        Returns:
            GoogleResponse: Updated response after navigating to the next page, or None if out of range.
        """
        return await self._navigate_page(resp, 1)

    async def search(
        self, url: Optional[str] = None, file: Union[str, bytes, Path, None] = None
    ) -> GoogleResponse:
        """Performs a reverse image search on Google.

        Supports searching by image URL or by uploading an image file.

        Requires either 'url' or 'file' to be provided.

        Args:
            url: URL of the image to search.
            file: Local image file (path or bytes) to search.

        Returns:
            GoogleResponse: Contains search results and additional information.

        Raises:
            ValueError: If neither 'url' nor 'file' is provided.
        """
        _url = self.base_url if url else f"{self.base_url}/upload"
        params: dict[str, Any] = {"sbisrc": 1, "safe": "off"}
        if url:
            params["image_url"] = url
            resp = await self.get(_url, params=params)
        elif file:
            files = {"encoded_image": read_file(file)}
            resp = await self.post(_url, data=params, files=files)
        else:
            raise ValueError("Either 'url' or 'file' must be provided")
        return GoogleResponse(resp.text, resp.url)
