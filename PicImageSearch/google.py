from pathlib import Path
from typing import Any, Dict, Optional, Union

from .model import GoogleResponse
from .network import HandOver


class Google(HandOver):
    """API client for the Google image search engine.

    Used for performing reverse image searches using Google service.

    Attributes:
         base_url: The base URL for Google searches, configurable for different regions.
            Example: `https://www.google.co.jp/searchbyimage` for searches in Japan.
    """

    def __init__(
        self,
        base_url: str = "https://www.google.com/searchbyimage",
        **request_kwargs: Any,
    ):
        """Initializes a Google API client with specified configurations.

        Args:
            base_url: The base URL for Google searcher, defaults to the international version.
            **request_kwargs: Additional arguments for network requests.
        """
        super().__init__(**request_kwargs)
        self.base_url = base_url

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
        params: Dict[str, Any] = {"sbisrc": 1}
        if url:
            params["image_url"] = url
            resp = await self.get(self.base_url, params=params)
        elif file:
            files = {
                "encoded_image": file if isinstance(file, bytes) else open(file, "rb")
            }
            resp = await self.post(f"{self.base_url}/upload", data=params, files=files)
        else:
            raise ValueError("Either 'url' or 'file' must be provided")
        return GoogleResponse(resp.text, resp.url)
