import asyncio
from json import loads as json_loads
from pathlib import Path
from typing import Any, Dict, Optional, Union

from .model import TraceMoeItem, TraceMoeMe, TraceMoeResponse
from .network import HandOver

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
    """API Client for the TraceMoe API to search anime by image.

    Inherits from HandOver for network operations.

    Attributes:
        search_url: A string representing the API endpoint for searching.
        me_url: A string representing the API endpoint to retrieve user info.
        size: An optional string indicating the size of the preview (s/m/l).
        mute: A boolean indicating whether to mute the preview video.
    """

    search_url = "https://api.trace.moe/search"
    me_url = "https://api.trace.moe/me"

    def __init__(
        self, mute: bool = False, size: Optional[str] = None, **request_kwargs: Any
    ):
        """Initializes the TraceMoe client with optional settings.

        Args:
            mute: If True, mutes the preview video. Defaults to False.
            size: Defines the preview size. Can be 's', 'm', or 'l'.
            **request_kwargs: Additional keyword arguments for request settings.
        """
        super().__init__(**request_kwargs)
        self.size: Optional[str] = size
        self.mute: bool = mute

    async def me(self, key: Optional[str] = None) -> TraceMoeMe:
        """Retrieves information about the API key usage.

        Args:
            key: The API key for authentication.

        Returns:
            An instance of TraceMoeMe containing the user's information.

        Raises:
            HTTPError: If the request to the API fails.
        """
        params = {"key": key} if key else None
        resp = await self.get(self.me_url, params=params)
        return TraceMoeMe(json_loads(resp.text))

    @staticmethod
    def set_params(
        url: Optional[str],
        anilist_id: Optional[int],
        cut_borders: bool,
    ) -> Dict[str, Union[bool, int, str]]:
        """Constructs query parameters for API requests.

        Args:
            url: The image URL to search for.
            anilist_id: The Anilist ID to limit the search to.
            cut_borders: If True, trims the borders of the image.

        Returns:
            A dictionary with query parameters for the API request.
        """
        params: Dict[str, Union[bool, int, str]] = {}
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
        """Updates the anime information of a search result item.

        Args:
            item: The TraceMoeItem object to update with additional data.
            chinese_title: If True, retrieves the Chinese title if available.

        Raises:
            HTTPError: If the request to the API fails.
        """
        variables = {"id": item.anilist}
        url = "https://trace.moe/anilist/"
        item.anime_info = json_loads(
            (
                await self.post(
                    url=url, json={"query": ANIME_INFO_QUERY, "variables": variables}
                )
            )[0]
        )["data"]["Media"]
        item.idMal = item.anime_info[
            "idMal"
        ]  # 匹配的MyAnimelist ID见https://myanimelist.net/ (matched MyAnimelist ID)
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
        """Searches for anime using an image or URL.

        Args:
            url: URL of the image.
            file: Local image file path or image data.
            key: API key for authentication.
            anilist_id: Anilist ID to limit the search.
            chinese_title: Include Chinese title in the result if available.
            cut_borders: Trim image borders during search.

        Returns:
            A TraceMoeResponse object with search results.

        Raises:
            ValueError: If neither URL nor file is provided.
            HTTPError: If the request to the API fails.
        """
        headers = {"x-trace-key": key} if key else None
        files: Optional[Dict[str, Any]] = None
        if url:
            params = self.set_params(url, anilist_id, cut_borders)
        elif file:
            params = self.set_params(None, anilist_id, cut_borders)
            files = (
                {"file": file}
                if isinstance(file, bytes)
                else {"file": open(file, "rb")}
            )
        else:
            raise ValueError("url or file is required")
        resp = await self.post(
            self.search_url, headers=headers, params=params, files=files
        )
        result = TraceMoeResponse(json_loads(resp.text), self.mute, self.size)
        await asyncio.gather(
            *[self.update_anime_info(item, chinese_title) for item in result.raw]
        )
        return result
