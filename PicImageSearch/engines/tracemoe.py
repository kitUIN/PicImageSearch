import asyncio
from json import loads as json_loads
from pathlib import Path
from typing import Any, Optional, Union

from ..model import TraceMoeItem, TraceMoeMe, TraceMoeResponse
from ..utils import read_file
from .base import BaseSearchEngine

ANIME_INFO_QUERY = """
query ($id: Int) {
  Media (id: $id, type: ANIME) {
    id
    idMal
    title {
      native
      romaji
      english
    }
    type
    format
    startDate {
      year
      month
      day
    }
    endDate {
      year
      month
      day
    }
    coverImage {
      large
    }
    synonyms
    isAdult
  }
}
"""


class TraceMoe(BaseSearchEngine):
    """API Client for the TraceMoe image search engine.

    Used for performing reverse image searches using TraceMoe service.

    Attributes:
        anilist_url: URL for TraceMoe endpoint to retrieve anime info.
        base_url: The base URL for TraceMoe searches.
        me_url: URL for TraceMoe API endpoint to retrieve user info.
        size: Optional string indicating preview size ('s', 'm', 'l').
        mute: A flag to mute preview video in search results.
    """

    def __init__(
        self,
        base_url: str = "https://trace.moe",
        base_url_api: str = "https://api.trace.moe",
        mute: bool = False,
        size: Optional[str] = None,
        **request_kwargs: Any,
    ):
        """Initializes a TraceMoe API client with specified configurations.

        Args:
            base_url: The base URL for TraceMoe searches.
            base_url_api: The base URL for TraceMoe API searches.
            mute: If True, mutes preview video in search results.
            size: Specifies preview video size ('s', 'm', 'l').
            **request_kwargs: Additional arguments for network requests.
        """
        self.anilist_url = f"{base_url}/anilist"
        base_url = f"{base_url_api}/search"
        super().__init__(base_url, **request_kwargs)
        self.me_url = f"{base_url_api}/me"
        self.mute: bool = mute
        self.size: Optional[str] = size

    async def me(self, key: Optional[str] = None) -> TraceMoeMe:
        """Retrieves user account information and API usage statistics from TraceMoe.

        Args:
            key: Optional API key for authentication. If not provided, uses anonymous access.

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
        resp = await self.get(self.me_url, params=params)
        return TraceMoeMe(json_loads(resp.text))

    @staticmethod
    def set_params(
        url: Optional[str],
        anilist_id: Optional[int],
        cut_borders: bool,
    ) -> dict[str, Union[bool, int, str]]:
        """Constructs query parameters for TraceMoe API request.

        Args:
            url: URL of the image to search. Optional if uploading a file.
            anilist_id: Anilist ID to limit search scope to a specific anime.
            cut_borders: If True, removes black borders from image before searching.

        Returns:
            dict[str, Union[bool, int, str]]: A dictionary containing:
                - 'url': Image URL if provided
                - 'cutBorders': Border cutting preference
                - 'anilistID': Specific anime ID if provided

        Note:
            Parameters are only included in the result if they have valid values.
        """
        params: dict[str, Union[bool, int, str]] = {}
        if cut_borders:
            params["cutBorders"] = "true"
        if anilist_id:
            params["anilistID"] = anilist_id
        if url:
            params["url"] = url
        return params

    async def update_anime_info(
        self, item: TraceMoeItem, chinese_title: bool = True
    ) -> None:
        """Updates a TraceMoeItem with detailed anime information from AniList API.

        Args:
            item: TraceMoeItem instance to be updated with detailed information.
            chinese_title: If True, attempts to fetch Chinese title if available.

        Note:
            Updates multiple fields including:
            - MAL and AniList IDs
            - Titles (native, romaji, english, chinese)
            - Anime metadata (type, format, dates)
            - Cover image URL
            - Adult content flag
            - Alternative titles (synonyms)
        """
        variables = {"id": item.anilist}
        item.anime_info = json_loads(
            (
                await self.post(
                    url=self.anilist_url,
                    json={"query": ANIME_INFO_QUERY, "variables": variables},
                )
            )[0]
        )["data"]["Media"]
        # Update item fields with anime information
        item.idMal = item.anime_info["idMal"]
        item.title = item.anime_info["title"]
        item.title_native = item.anime_info["title"]["native"]
        item.title_romaji = item.anime_info["title"]["romaji"]
        item.title_english = item.anime_info["title"]["english"]
        item.synonyms = item.anime_info["synonyms"]
        item.isAdult = item.anime_info["isAdult"]
        item.type = item.anime_info["type"]
        item.format = item.anime_info["format"]
        item.start_date = item.anime_info["startDate"]
        item.end_date = item.anime_info["endDate"]
        item.cover_image = item.anime_info["coverImage"]["large"]
        if chinese_title:
            item.title_chinese = item.anime_info["title"].get("chinese", "")

    async def search(
        self,
        url: Optional[str] = None,
        file: Union[str, bytes, Path, None] = None,
        key: Optional[str] = None,
        anilist_id: Optional[int] = None,
        chinese_title: bool = True,
        cut_borders: bool = True,
        **kwargs: Any,
    ) -> TraceMoeResponse:
        """Performs a reverse image search for anime scenes using TraceMoe.

        This method supports two ways of searching:
        1. Search by image URL
        2. Search by uploading a local image file

        Args:
            url: URL of the image to search.
            file: Local image file (path string, bytes data, or Path object).
            key: Optional API key for authentication and higher quotas.
            anilist_id: Optional AniList ID to limit search scope.
            chinese_title: If True, includes Chinese titles in results.
            cut_borders: If True, removes black borders before searching.
            **kwargs: Additional arguments passed to the parent class.

        Returns:
            TraceMoeResponse: Search results containing:
                - List of matching anime scenes
                - Confidence scores
                - Time stamps
                - Preview URLs
                - Detailed anime information

        Raises:
            ValueError: If neither 'url' nor 'file' is provided.

        Note:
            - Only one of 'url' or 'file' should be provided
            - Using an API key increases search quota and priority
            - Results are automatically enriched with detailed anime information
        """
        await super().search(url, file, **kwargs)

        headers = {"x-trace-key": key} if key else None
        files: Optional[dict[str, Any]] = None

        if url:
            params = self.set_params(url, anilist_id, cut_borders)
        else:
            params = self.set_params(None, anilist_id, cut_borders)
            files = {"file": read_file(file)}

        resp = await self._make_request(
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
        await asyncio.gather(
            *[self.update_anime_info(item, chinese_title) for item in result.raw]
        )

        return result