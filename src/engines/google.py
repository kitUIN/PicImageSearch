from pathlib import Path
from typing import Any, Optional, Union

from ..model import GoogleResponse
from ..utils import read_file
from .base import BaseSearchEngine


class Google(BaseSearchEngine):
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
        base_url = f"{base_url}/searchbyimage"
        super().__init__(base_url, **request_kwargs)

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
        next_page_number = resp.page_number + offset
        if next_page_number < 1 or next_page_number > len(resp.pages):
            return None
        _resp = await self.get(resp.pages[next_page_number - 1])
        return GoogleResponse(_resp.text, _resp.url, next_page_number, resp.pages)

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

    async def _ensure_thumbnail_data(self, resp: GoogleResponse) -> GoogleResponse:
        """Ensures the response contains thumbnail data.

        If the initial response lacks thumbnail data, an additional request is made to fetch complete data.

        Args:
            resp: The initial GoogleResponse instance.

        Returns:
            GoogleResponse: A response containing thumbnail data.
        """
        if resp and resp.raw:
            selected = next((i for i in resp.raw if i.thumbnail), resp.raw[0])
            if not selected.thumbnail and len(resp.raw) > 1:
                _resp = await self.get(resp.url)
                return GoogleResponse(_resp.text, _resp.url)
        return resp

    async def search(
        self,
        url: Optional[str] = None,
        file: Union[str, bytes, Path, None] = None,
        **kwargs: Any,
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
        await super().search(url, file, **kwargs)

        params: dict[str, Any] = {"sbisrc": 1, "safe": "off"}

        if url:
            params["image_url"] = url
            resp = await self._make_request(method="get", params=params)
        else:
            files = {"encoded_image": read_file(file)}
            resp = await self._make_request(
                method="post",
                endpoint="upload",
                data=params,
                files=files,
            )

        initial_resp = GoogleResponse(resp.text, resp.url)
        return await self._ensure_thumbnail_data(initial_resp)
