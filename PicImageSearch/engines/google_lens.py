from pathlib import Path
from typing import Any, Literal, Optional, Union

from pyquery import PyQuery
from typing_extensions import override

from ..model import GoogleLensExactMatchesResponse, GoogleLensResponse
from ..network import RESP
from ..utils import read_file
from .base import BaseSearchEngine


class GoogleLens(BaseSearchEngine[Union[GoogleLensResponse, GoogleLensExactMatchesResponse]]):
    """API client for the Google Lens image search engine.

    Supported search types:
        - all:  Returns all types of results (default).
        - products: Returns product-related results.
        - visual_matches: Returns visually similar images.
        - exact_matches: Returns pages with exact matches of the image.

    Attributes:
        base_url (str): The base URL for Google Lens searches.
        search_url (str): The base URL for Google search results.
        hl_param (str): The language parameter combined with country code.
        search_type (str): The type of search to perform ('all', 'products', 'visual_matches', 'exact_matches').
        q (Optional[str]): Optional query parameter for search. Not applicable for 'exact_matches' type.
    """

    def __init__(
        self,
        base_url: str = "https://lens.google.com",
        search_url: str = "https://www.google.com",
        search_type: Literal["all", "products", "visual_matches", "exact_matches"] = "all",
        q: Optional[str] = None,
        hl: str = "en",
        country: str = "US",
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
            hl (str): The hl parameter for language. Defaults to "en". See
                https://www.searchapi.io/docs/parameters/google/hl for options.
            country (str): The country parameter for regional settings. Defaults to "US". See
                https://www.searchapi.io/docs/parameters/google-lens/country for options.
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
        self.hl_param: str = f"{hl}-{country.upper()}"
        self.search_type: str = search_type
        self.q: Optional[str] = q

    async def _perform_image_search(
        self,
        url: Optional[str] = None,
        file: Union[str, bytes, Path, None] = None,
        q: Optional[str] = None,
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
        params = {"hl": self.hl_param}
        if q and self.search_type != "exact_matches":
            params["q"] = q

        if file:
            endpoint = "v3/upload"
            filename = "image.jpg" if isinstance(file, bytes) else Path(file).name
            files = {"encoded_image": (filename, read_file(file), "image/jpeg")}
            resp = await self._send_request(
                method="post",
                endpoint=endpoint,
                params=params,
                files=files,
            )
        elif url:
            endpoint = "uploadbyurl"
            params["url"] = url
            resp = await self._send_request(
                method="post" if file else "get",
                endpoint=endpoint,
                params=params,
            )
        else:
            raise ValueError("Either 'url' or 'file' must be provided")

        dom = PyQuery(resp.text)
        exact_link = ""

        if self.search_type != "all":
            if udm_value := {
                "products": "37",
                "visual_matches": "44",
                "exact_matches": "48",
            }.get(self.search_type):
                exact_link = dom(f'a[href*="udm={udm_value}"]').attr("href") or ""

        if exact_link:
            return await self._send_request(method="get", url=f"{self.search_url}{exact_link}")
        return resp

    @override
    async def search(
        self,
        url: Optional[str] = None,
        file: Union[str, bytes, Path, None] = None,
        q: Optional[str] = None,
        **kwargs: Any,
    ) -> Union[GoogleLensResponse, GoogleLensExactMatchesResponse]:
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
        if q is not None and self.search_type == "exact_matches":
            q = None

        resp = await self._perform_image_search(url, file, q)

        if self.search_type == "exact_matches":
            return GoogleLensExactMatchesResponse(resp.text, resp.url)
        else:
            return GoogleLensResponse(resp.text, resp.url)
