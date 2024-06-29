import asyncio
from json import loads as json_loads
from pathlib import Path
from typing import Any, Optional, Union

from .model import TraceMoeItem, TraceMoeMe, TraceMoeResponse
from .network import HandOver
from .utils import read_file

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


class TraceMoe(HandOver):
    """API Client for the TraceMoe image search engine.

    Used for performing reverse image searches using TraceMoe service.

    Attributes:
        base_url: The base URL for TraceMoe searches.
        search_url: URL for TraceMoe API endpoint for image search.
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
        super().__init__(**request_kwargs)
        self.base_url = base_url
        self.search_url = f"{base_url_api}/search"
        self.me_url = f"{base_url_api}/me"
        self.mute: bool = mute
        self.size: Optional[str] = size

    async def me(self, key: Optional[str] = None) -> TraceMoeMe:
        """Retrieves information about the user's API key usage from TraceMoe.

        Args:
            key: Optional API key for authentication.

        Returns:
            TraceMoeMe: Information about the user's API key usage.
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
            url: URL of the image to search.
            anilist_id: Anilist ID for specific anime focus.
            cut_borders: If True, trims image borders during search.

        Returns:
            dict[str, Union[bool, int, str]]: Query parameters for the API request.
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
        """Updates TraceMoeItem with detailed anime information from TraceMoe API.

        Args:
            item: TraceMoeItem to update with anime information.
            chinese_title: If True, includes Chinese title in item info.
        """
        variables = {"id": item.anilist}
        url = f"{self.base_url}/anilist/"
        item.anime_info = json_loads(
            (
                await self.post(
                    url=url, json={"query": ANIME_INFO_QUERY, "variables": variables}
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
    ) -> TraceMoeResponse:
        """Performs a reverse image search on TraceMoe.

        Supports searching by image URL or by uploading an image file.

        Requires either 'url' or 'file' to be provided.

        Args:
            url: URL of the image to search.
            file: Local image file (path or bytes) to search.
            key: Optional API key for authentication.
            anilist_id: Anilist ID to limit search scope.
            chinese_title: If True, includes Chinese titles in results.
            cut_borders: If True, trims image borders for search.

        Returns:
            TraceMoeResponse: Search results and additional metadata.

        Raises:
            ValueError: If neither 'url' nor 'file' is provided.
        """
        headers = {"x-trace-key": key} if key else None
        files: Optional[dict[str, Any]] = None
        if url:
            params = self.set_params(url, anilist_id, cut_borders)
        elif file:
            params = self.set_params(None, anilist_id, cut_borders)
            files = {"file": read_file(file)}
        else:
            raise ValueError("Either 'url' or 'file' must be provided")
        resp = await self.post(
            self.search_url, headers=headers, params=params, files=files
        )
        result = TraceMoeResponse(json_loads(resp.text), self.mute, self.size)
        await asyncio.gather(
            *[self.update_anime_info(item, chinese_title) for item in result.raw]
        )
        return result
