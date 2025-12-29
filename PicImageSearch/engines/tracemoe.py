from json import loads as json_loads
from pathlib import Path
from typing import Any

from typing_extensions import override

from ..model import TraceMoeMe, TraceMoeResponse
from ..utils import read_file
from .base import BaseSearchEngine


class TraceMoe(BaseSearchEngine[TraceMoeResponse]):
    """API Client for the TraceMoe image search engine.

    Used for performing reverse image searches using TraceMoe service.

    Attributes:
        base_url (str): The base URL for TraceMoe searches.
        me_url (str): URL for TraceMoe API endpoint to retrieve user info.
        size (Optional[str]): Optional string indicating preview size ('s', 'm', 'l').
        mute (bool): A flag to mute preview video in search results.
    """

    def __init__(
        self,
        base_url: str = "https://trace.moe",
        base_url_api: str = "https://api.trace.moe",
        mute: bool = False,
        size: str | None = None,
        **request_kwargs: Any,
    ):
        """Initializes a TraceMoe API client with specified configurations.

        Args:
            base_url (str): The base URL for TraceMoe searches.
            base_url_api (str): The base URL for TraceMoe API searches.
            mute (bool): If True, mutes preview video in search results.
            size (Optional[str]): Specifies preview video size ('s', 'm', 'l').
            **request_kwargs (Any): Additional arguments for network requests.
        """
        base_url = f"{base_url_api}/search"
        super().__init__(base_url, **request_kwargs)
        self.me_url: str = f"{base_url_api}/me"
        self.mute: bool = mute
        self.size: str | None = size

    async def me(self, key: str | None = None) -> TraceMoeMe:
        """Retrieves user account information and API usage statistics from TraceMoe.

        Args:
            key (Optional[str]): Optional API key for authentication. If not provided, uses anonymous access.

        Returns:
            TraceMoeMe: An object containing:
                - User's API quota information
                - Search quota limits
                - Priority status
                - API key validity status

        Note:
            Response data includes search quota reset time and remaining searches.
        """
        params = {"key": key} if key else None
        resp = await self._send_request(method="get", url=self.me_url, params=params)
        return TraceMoeMe(json_loads(resp.text))

    @override
    async def search(
        self,
        url: str | None = None,
        file: str | bytes | Path | None = None,
        key: str | None = None,
        anilist_id: int | None = None,
        chinese_title: bool = True,
        cut_borders: bool = True,
        **kwargs: Any,
    ) -> TraceMoeResponse:
        """Performs a reverse image search for anime scenes using TraceMoe.

        This method supports two ways of searching:
            1. Search by image URL
            2. Search by uploading a local image file

        Args:
            url (Optional[str]): URL of the image to search.
            file (Union[str, bytes, Path, None]): Local image file (path string, bytes data, or Path object).
            key (Optional[str]): Optional API key for authentication and higher quotas.
            anilist_id (Optional[int]): Optional AniList ID to limit search scope.
            chinese_title (bool): If True, includes Chinese titles in results.
            cut_borders (bool): If True, removes black borders before searching.
            **kwargs (Any): Additional arguments passed to the parent class.

        Returns:
            TraceMoeResponse: Search results containing:
                - List of matching anime scenes
                - Confidence scores
                - Time stamps
                - Preview URLs
                - Detailed anime information

        Raises:
            ValueError: If neither `url` nor `file` is provided.

        Note:
            - Only one of `url` or `file` should be provided
            - Using an API key increases search quota and priority
            - Results are automatically enriched with detailed anime information
        """
        headers = {"x-trace-key": key} if key else None
        files: dict[str, Any] | None = None

        # Add anilistInfo parameter to get anime info directly from TraceMoe API
        params: dict[str, bool | int | str] = {"anilistInfo": ""}
        if cut_borders:
            params["cutBorders"] = "true"
        if anilist_id:
            params["anilistID"] = anilist_id

        if url:
            params["url"] = url
        elif file:
            files = {"file": read_file(file)}
        else:
            raise ValueError("Either 'url' or 'file' must be provided")

        resp = await self._send_request(
            method="post",
            headers=headers,
            params=params,
            files=files,
        )

        result = TraceMoeResponse(
            resp_data=json_loads(resp.text),
            resp_url=resp.url,
            mute=self.mute,
            size=self.size,
        )

        return result
