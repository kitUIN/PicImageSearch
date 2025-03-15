from typing import Any

from typing_extensions import override

from ..types import DomainInfo
from .base import BaseSearchItem, BaseSearchResponse


class TineyeItem(BaseSearchItem):
    """Represents a single Tineye search result item.

    A class that processes and stores individual search result data from Tineye reverse image search.

    Attributes:
        thumbnail (str): URL of the thumbnail image.
        image_url (str): Direct URL to the full-size image.
        url (str): URL of the webpage where the image was found (backlink).
        domain (str): Domain of the webpage.
        size (list[int]): Dimensions of the image as [width, height].
        crawl_date (str): Timestamp indicating when the image was crawled by Tineye.
    """

    def __init__(self, data: dict[str, Any], **kwargs: Any):
        """Initializes a TineyeItem with data from a search result.

        Args:
            data (dict[str, Any]): A dictionary containing the search result data.
        """
        super().__init__(data, **kwargs)

    @override
    def _parse_data(self, data: dict[str, Any], **kwargs: Any) -> None:
        """Parses the raw data for a single Tineye search result."""
        self.thumbnail: str = data["image_url"]
        self.image_url: str = data["backlinks"][0]["url"]
        self.url: str = data["backlinks"][0]["backlink"]
        self.domain: str = data["domain"]
        self.size: list[int] = [data["width"], data["height"]]
        self.crawl_date: str = data["backlinks"][0]["crawl_date"]


class TineyeResponse(BaseSearchResponse[TineyeItem]):
    """Represents a complete Tineye search response.

    Attributes:
        origin (dict): The raw JSON response data from Tineye.
        raw (list[TineyeItem]): List of TineyeItem objects, each representing a search result.
        domains (dict[str, int]):  A dictionary where keys are the domains where the image was found,
            and values are the number of matches found on that domain. Only available after the initial search.
        query_hash (str): Unique identifier for the search query. Used for pagination.
        status_code (int): HTTP status code of the response.
        page_number (int): Current page number.
        url (str): URL of the initial search results page.
    """

    def __init__(
        self,
        resp_data: dict[str, Any],
        resp_url: str,
        domains: list[DomainInfo],
        page_number: int = 1,
    ):
        """Initializes a TineyeResponse object with response data and metadata.

        Args:
            resp_data (dict[str, Any]):
            resp_url (str):
            page_number (int):
        """
        super().__init__(
            resp_data,
            resp_url,
            domains=domains,
            page_number=page_number,
        )
        self.domains: list[DomainInfo] = domains
        self.page_number: int = page_number

    @override
    def _parse_response(self, resp_data: dict[str, Any], **kwargs: Any) -> None:
        """Parses the raw JSON response from Tineye."""
        self.query_hash: str = resp_data["query_hash"]
        self.status_code: int = resp_data["status_code"]
        self.total_pages: int = resp_data["total_pages"]
        matches = resp_data["matches"]
        self.raw: list[TineyeItem] = [TineyeItem(i) for i in matches] if matches else []
