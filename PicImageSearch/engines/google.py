from pathlib import Path
from typing import Any, Optional, Union

from typing_extensions import override

from ..model import GoogleResponse
from ..utils import read_file
from .base import BaseSearchEngine


class Google(BaseSearchEngine[GoogleResponse]):
    """API client for the Google image search engine.

    Used for performing reverse image searches using Google service.

    Attributes:
        base_url (str): The base URL for Google searches, configurable for different regions.
            Example: `https://www.google.co.jp` for searches in Japan.
    """

    def __init__(
        self,
        base_url: str = "https://www.google.com",
        **request_kwargs: Any,
    ):
        """Initializes a Google API client with specified configurations.

        Args:
            base_url (str): The base URL for Google searches, defaults to the international version.
            **request_kwargs (Any): Additional arguments for network requests.
        """
        base_url = f"{base_url}/searchbyimage"
        super().__init__(base_url, **request_kwargs)

    async def _navigate_page(self, resp: GoogleResponse, offset: int) -> Optional[GoogleResponse]:
        """Navigates to a specific page in search results.

        This method handles both forward and backward navigation through search results.

        Args:
            resp (GoogleResponse): The current GoogleResponse instance containing page information.
            offset (int): Integer indicating navigation direction and distance:
                - Positive values move forward
                - Negative values move backward
                - Magnitude indicates number of pages to move

        Returns:
            Optional[GoogleResponse]:
                - New GoogleResponse instance after navigation
                - None if target page is out of valid range (< 1 or > total pages)

        Note:
            The method maintains page history and updates page numbers automatically.
        """
        next_page_number = resp.page_number + offset
        if next_page_number < 1 or next_page_number > len(resp.pages):
            return None

        _resp = await self._send_request(method="get", url=resp.pages[next_page_number - 1])
        return GoogleResponse(_resp.text, _resp.url, next_page_number, resp.pages)

    async def pre_page(self, resp: GoogleResponse) -> Optional[GoogleResponse]:
        """Navigates to the previous page in Google search results.

        Args:
            resp (GoogleResponse): The current GoogleResponse instance.

        Returns:
            GoogleResponse: Updated response after navigating to the previous page, or None if out of range.
        """
        return await self._navigate_page(resp, -1)

    async def next_page(self, resp: GoogleResponse) -> Optional[GoogleResponse]:
        """Navigates to the next page in Google search results.

        Args:
            resp (GoogleResponse): The current GoogleResponse instance.

        Returns:
            GoogleResponse: Updated response after navigating to the next page, or None if out of range.
        """
        return await self._navigate_page(resp, 1)

    async def _ensure_thumbnail_data(self, resp: GoogleResponse) -> GoogleResponse:
        """Ensures the response contains valid thumbnail data by making additional requests if needed.

        This method performs the following:
            1. Checks if response contains raw data
            2. Attempts to find first result with thumbnail
            3. Makes an additional request if no thumbnail is found

        Args:
            resp (GoogleResponse): The initial GoogleResponse instance to check for thumbnail data

        Returns:
            GoogleResponse:
                - Original response if thumbnail data exists
                - New response with thumbnail data after additional request
                - Original response if no thumbnail data can be found

        Note:
            This is an internal method used by the search method to ensure complete results.
        """
        if resp and resp.raw:
            selected = next((i for i in resp.raw if i.thumbnail), resp.raw[0])
            if not selected.thumbnail and len(resp.raw) > 1:
                _resp = await self._send_request(method="get", url=resp.url)
                return GoogleResponse(_resp.text, _resp.url)
        return resp

    @override
    async def search(
        self,
        url: Optional[str] = None,
        file: Union[str, bytes, Path, None] = None,
        **kwargs: Any,
    ) -> GoogleResponse:
        """Performs a reverse image search on Google.

        This method supports two ways of searching:
            1. Search by image URL
            2. Search by uploading a local image file

        Args:
            url (Optional[str]): URL of the image to search
            file (Union[str, bytes, Path, None]): Local image file, which can be:
                - Path string
                - Bytes data
                - Path object
            **kwargs (Any): Additional arguments passed to the parent class

        Returns:
            GoogleResponse: A response object containing:
                - Search results
                - Thumbnail data
                - Page navigation information
                - Raw response data

        Raises:
            ValueError: If neither `url` nor `file` is provided

        Note:
            - Only one of `url` or `file` should be provided
            - The method automatically ensures thumbnail data is present in results
            - Safe search is disabled by default
        """
        params: dict[str, Any] = {"sbisrc": 1, "safe": "off"}

        if url:
            params["image_url"] = url
            resp = await self._send_request(method="get", params=params)
        elif file:
            files = {"encoded_image": read_file(file)}
            resp = await self._send_request(
                method="post",
                endpoint="upload",
                data=params,
                files=files,
            )
        else:
            raise ValueError("Either 'url' or 'file' must be provided")

        initial_resp = GoogleResponse(resp.text, resp.url)
        return await self._ensure_thumbnail_data(initial_resp)
