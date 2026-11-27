import re
from pathlib import Path
from typing import Any, Literal
from urllib.parse import urlparse

from pyquery import PyQuery
from typing_extensions import override

from ..model import GoogleLensExactMatchesResponse, GoogleLensResponse
from ..network import RESP
from ..utils import read_file
from .base import BaseSearchEngine


class GoogleLens(BaseSearchEngine[GoogleLensResponse | GoogleLensExactMatchesResponse]):
    """API client for the Google Lens image search engine.

    Supported search types:
        - all:  Returns all types of results (default).
        - products: Returns product-related results.
        - visual_matches: Returns visually similar images.
        - exact_matches: Returns pages with exact matches of the image.

    Attributes:
        base_url (str): The base URL for Google Lens searches.
        search_url (str): The base URL for Google search results.
        search_type (str): The type of search to perform ('all', 'products', 'visual_matches', 'exact_matches').
        q (Optional[str]): Optional query parameter for search. Not applicable for 'exact_matches' type.
        ai_overview (bool): Whether to load the AI overview for 'all' search type.
    """

    def __init__(
        self,
        base_url: str = "https://lens.google.com",
        search_url: str = "https://www.google.com",
        search_type: Literal["all", "products", "visual_matches", "exact_matches"] = "all",
        q: str | None = None,
        ai_overview: bool = False,
        **request_kwargs: Any,
    ):
        """Initializes a GoogleLens API client with specified configurations.

        Args:
            base_url (str): The base URL for Google Lens searches. Defaults to "https://lens.google.com".
            search_url (str): The base URL for Google search results. Defaults to "https://www.google.com".
            search_type (Literal["all", "products", "visual_matches", "exact_matches"]): The type of search to perform.
                Defaults to "all".
            q (Optional[str]): Optional query parameter for search. Defaults to None. Not applicable for 'exact_matches'
                type.
            ai_overview (bool): If True, load the AI overview with an extra request. Only applies to 'all' search_type.
                Defaults to False.
            **request_kwargs (Any): Additional arguments for network requests.

        Raises:
            ValueError: If search_type is 'exact_matches' and q is provided.
            ValueError: If search_type is not one of 'all', 'products', 'visual_matches', 'exact_matches'.
        """
        super().__init__(base_url, **request_kwargs)

        valid_search_types = ["all", "products", "visual_matches", "exact_matches"]
        if search_type not in valid_search_types:
            raise ValueError(f"Invalid search_type: {search_type}. Must be one of {valid_search_types}")
        if search_type == "exact_matches" and q:
            raise ValueError("Query parameter 'q' is not applicable for 'exact_matches' search_type.")

        self.search_url: str = search_url
        self.search_type: str = search_type
        self.q: str | None = q
        self.ai_overview: bool = ai_overview

    async def _perform_image_search(
        self,
        url: str | None = None,
        file: str | bytes | Path | None = None,
        q: str | None = None,
    ) -> RESP:
        """Uploads an image (URL or file) to Google Lens and returns the response from the search result page.

        Args:
            url (Optional[str]): URL of the image to search.
            file (Union[str, bytes, Path, None]): Path to the image file, bytes data, or Path object.
            q (Optional[str]): Optional query parameter for search. Overrides the instance's q attribute if provided.
                Will be ignored for 'exact_matches' search type.

        Returns:
            RESP: Response object containing the HTML content, URL and status code of the search result page.

        Raises:
            ValueError: If neither 'url' nor 'file' is provided.
        """
        # Google Lens currently returns 403 when upload requests include `hl`.
        params: dict[str, str] = {}
        if q and self.search_type != "exact_matches":
            params["q"] = q

        if file:
            filename = "image.jpg" if isinstance(file, bytes) else Path(file).name
            files = {"encoded_image": (filename, read_file(file), "image/jpeg")}
            resp = await self._send_request(
                method="post",
                endpoint="v3/upload",
                params=params,
                files=files,
            )
        elif url:
            params["url"] = url
            resp = await self._send_request(
                method="get",
                endpoint="uploadbyurl",
                params=params,
            )
            if urlparse(resp.url).hostname == "accounts.google.com":
                return await self._perform_image_search(file=await self.download(url), q=q)
        else:
            raise ValueError("Either 'url' or 'file' must be provided")

        dom = PyQuery(resp.text)
        udm_value = {
            "products": "37",
            "visual_matches": "44",
            "exact_matches": "48",
        }.get(self.search_type)
        if udm_value and (exact_link := dom(f'a[href*="udm={udm_value}"]').attr("href")):
            return await self._send_request(method="get", url=f"{self.search_url}{exact_link}")

        return resp

    @override
    async def search(
        self,
        url: str | None = None,
        file: str | bytes | Path | None = None,
        q: str | None = None,
        **kwargs: Any,
    ) -> GoogleLensResponse | GoogleLensExactMatchesResponse:
        """Performs a reverse image search on Google Lens.

        This method supports searching by image URL or by uploading a local image file.

        Args:
            url (Optional[str]): URL of the image to search.
            file (Union[str, bytes, Path, None]): Local image file, can be a path string, bytes data, or Path object.
            q (Optional[str]): Optional query parameter for search. Overrides the instance's q attribute if provided.
                Will be ignored for 'exact_matches' search type.
            **kwargs (Any): Additional arguments passed to the underlying request.

        Returns:
            Union[GoogleLensResponse, GoogleLensExactMatchesResponse]: An object containing search results.
                Returns GoogleLensExactMatchesResponse for 'exact_matches' search_type, and
                GoogleLensResponse for others.

        Raises:
            ValueError: If neither `url` nor `file` is provided.
        """
        search_q = q if q is not None else self.q
        if self.search_type == "exact_matches":
            search_q = None
        resp = await self._perform_image_search(url, file, search_q)

        if self.search_type == "exact_matches":
            return GoogleLensExactMatchesResponse(resp.text, resp.url)

        ai_overview = None
        if self.ai_overview and (match := re.search(r"url:'(/async/folsrch\?[^']+)'", resp.text)):
            ai_overview_url = match[1].encode().decode("unicode_escape")
            ai_overview = (await self._send_request(method="get", url=f"{self.search_url}{ai_overview_url}")).text

        return GoogleLensResponse(resp.text, resp.url, ai_overview=ai_overview)
