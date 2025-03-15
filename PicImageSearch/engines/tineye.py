from json import loads as json_loads
from pathlib import Path
from typing import Any, Optional, Union

from typing_extensions import override

from ..model import TineyeResponse
from ..types import DomainInfo
from ..utils import deep_get, read_file
from .base import BaseSearchEngine


class Tineye(BaseSearchEngine[TineyeResponse]):
    """API client for the Tineye reverse image search engine.

    Tineye is a reverse image search engine that allows you to find where an image appears on the web.
    This client provides methods for searching by image URL or by uploading a local image file,
    and retrieving matching images along with their domains and counts.

    Attributes:
        base_url (str): The base URL for Tineye searches. Defaults to "https://tineye.com".
    """

    def __init__(self, base_url: str = "https://tineye.com", **request_kwargs: Any):
        """Initializes a Tineye API client.

        Args:
            base_url (str): The base URL for Tineye searches.
            **request_kwargs (Any): Additional keyword arguments passed to the underlying network client.
        """
        super().__init__(base_url, **request_kwargs)

    async def _get_domains(self, query_hash: str) -> list[DomainInfo]:
        """Retrieves domain information for a given query hash.

        Args:
            query_hash (str): The unique identifier for the search query.

        Returns:
            list[DomainInfo]: A list of domain information objects containing domain name,
            match count and optional tag.
        """
        resp = await self._send_request(method="get", endpoint=f"api/v1/search/get_domains/{query_hash}")
        resp_json = json_loads(resp.text)

        return [DomainInfo.from_raw_data(domain_data) for domain_data in resp_json.get("domains", [])]

    async def _navigate_page(self, resp: TineyeResponse, offset: int) -> Optional[TineyeResponse]:
        """Navigates to a specific page in the Tineye search results.

        This internal method handles the pagination of Tineye results.  It calculates the URL for the target page
        based on the initial query parameters and fetches the results.

        Args:
            resp (TineyeResponse): The current `TineyeResponse` object containing pagination information.
            offset (int): The number of pages to move forward or backward. Positive values move forward,
                negative values move backward.

        Returns:
            Optional[TineyeResponse]: A new `TineyeResponse` object for the target page, or `None` if the target page
                is out of bounds (less than 1 or greater than the total number of pages).
        """
        next_page_number = resp.page_number + offset
        if next_page_number < 1 or next_page_number > resp.total_pages:
            return None

        api_url = resp.url.replace("search/", "api/v1/result_json/").replace(
            f"page={resp.page_number}", f"page={next_page_number}"
        )
        _resp = await self._send_request(method="get", url=api_url)
        resp_json = json_loads(_resp.text)
        resp_json.update({"status_code": _resp.status_code})

        return TineyeResponse(
            resp_json,
            _resp.url,
            resp.domains,
            next_page_number,
        )

    async def pre_page(self, resp: TineyeResponse) -> Optional[TineyeResponse]:
        """Navigates to the previous page of Tineye search results.

        Args:
            resp (TineyeResponse): The current `TineyeResponse` object.

        Returns:
            Optional[TineyeResponse]: A `TineyeResponse` object for the previous page, or `None` if there is no
                previous page.
        """
        return await self._navigate_page(resp, -1)

    async def next_page(self, resp: TineyeResponse) -> Optional[TineyeResponse]:
        """Navigates to the next page of Tineye search results.

        Args:
            resp (TineyeResponse): The current `TineyeResponse` object.

        Returns:
            Optional[TineyeResponse]: A `TineyeResponse` object for the next page, or `None` if there is no next page.
        """
        return await self._navigate_page(resp, 1)

    @override
    async def search(
        self,
        url: Optional[str] = None,
        file: Union[str, bytes, Path, None] = None,
        show_unavailable_domains: bool = False,
        domain: str = "",
        sort: str = "score",
        order: str = "desc",
        tags: str = "",
        **kwargs: Any,
    ) -> TineyeResponse:
        """Performs a reverse image search on Tineye.

        Searches for matching images on the web using either an image URL or a local image file.
        After the initial search, retrieves domain information for the matched images.


        Args:
            url (Optional[str]): The URL of the image to search for.
            file (Union[str, bytes, Path, None]): The local path to the image file to search for.
            show_unavailable_domains (bool): Whether to include results from unavailable domains.
                Defaults to False.
            domain (str):  Filter results to only include matches from this domain (only one domain is allowed).
                Defaults to "".
            sort (str): The sorting criteria for results. Can be "size", "score", or "crawl_date".
                Defaults to "score".
                - "score" (with `order="desc"`): Best match first (default).
                - "score" (with `order="asc"`): Most changed first.
                - "crawl_date" (with `order="desc"`): Newest images first.
                - "crawl_date" (with `order="asc"`): Oldest images first.
                - "size" (with `order="desc"`): Largest images first.
            order (str): The sorting order. Can be "asc" (ascending) or "desc" (descending). Defaults to "desc".
            tags (str):  Comma-separated tags to filter results. For example, "stock,collection". Defaults to "".
            **kwargs (Any): Additional keyword arguments passed to the underlying network client.

        Returns:
            TineyeResponse: A `TineyeResponse` object containing the search results, domain information, and metadata.

        Raises:
            ValueError: If neither `url` nor `file` is provided.

        Note:
            - Only one of `url` or `file` should be provided
        """
        files: Optional[dict[str, Any]] = None
        params: dict[str, Any] = {
            "sort": sort,
            "order": order,
            "page": 1,
            "show_unavailable_domains": show_unavailable_domains or "",
            "tags": tags,
            "domain": domain,
        }
        params = {k: v for k, v in params.items() if v}

        if url:
            params["url"] = url
        elif file:
            files = {"image": read_file(file)}
        else:
            raise ValueError("Either 'url' or 'file' must be provided")

        resp = await self._send_request(
            method="post",
            endpoint="api/v1/result_json/",
            data=params,
            files=files,
        )
        resp_json = json_loads(resp.text)
        resp_json["status_code"] = resp.status_code
        _url = resp.url

        domains = []
        if query_hash := deep_get(resp_json, "query.key"):
            query_string = "&".join(f"{k}={v}" for k, v in params.items())
            _url = f"{self.base_url}/search/{query_hash}?{query_string}"
            domains = await self._get_domains(resp_json["query"]["hash"])

        return TineyeResponse(resp_json, _url, domains)
