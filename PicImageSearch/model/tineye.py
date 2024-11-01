from typing import Any, Optional

from .base import BaseSearchItem, BaseSearchResponse


class TineyeItem(BaseSearchItem):
    """Represents a single Tineye search result item.

    Attributes:
        thumbnail (str): URL of the thumbnail image.
        image_url (str): Direct URL to the full-size image.
        url (str): URL of the webpage where the image was found (backlink).
        domain (str): Domain of the webpage.
        size (list[int]): Dimensions of the image as [width, height].
        crawl_date (str): Timestamp indicating when the image was crawled by Tineye.
    """

    def _parse_data(self, data: dict[str, Any], **kwargs: Any) -> None:
        """Parses the raw data for a single Tineye search result."""
        self.thumbnail: str = data["image_url"]
        self.image_url: str = data["backlinks"][0]["url"]
        self.url: str = data["backlinks"][0]["backlink"]
        self.domain: str = data["domain"]
        self.size: list[int] = [data["width"], data["height"]]
        self.crawl_date: str = data["backlinks"][0]["crawl_date"]


class TineyeResponse(BaseSearchResponse):
    """Represents a complete Tineye search response.

    Attributes:
        origin (dict): The raw JSON response data from Tineye.
        raw (list[TineyeItem]): List of TineyeItem objects, each representing a search result.
        domains (dict[str, int]):  A dictionary where keys are the domains where the image was found,
            and values are the number of matches found on that domain. Only available after the initial search.
        query_hash (str): Unique identifier for the search query. Used for pagination.
        status_code (int): HTTP status code of the response.
        pages (list[str]): URLs of all paginated result pages.
        page_number (int): Current page number.
        url (str): URL of the initial search results page.
        show_unavailable_domains (bool): Whether unavailable domains are included in results.
    """

    def __init__(
        self,
        resp_data: dict[str, Any],
        resp_url: str,
        page_number: int = 1,
        pages: Optional[list[str]] = None,
        query_hash: Optional[str] = None,
        show_unavailable_domains: bool = False,
        domains: Optional[dict[str, int]] = None,
        **kwargs,
    ):
        """Initializes a TineyeResponse object with response data and metadata."""
        self.query_hash = query_hash
        self.show_unavailable_domains = True if show_unavailable_domains else False
        self.domains = domains
        super().__init__(resp_data, resp_url, page_number=page_number, pages=pages, **kwargs)

    def _parse_response(self, resp_data: dict[str, Any], **kwargs: Any) -> None:
        """Parses the raw JSON response from Tineye."""
        self.query_hash: str = resp_data.get("query_hash")
        self.status_code: int = resp_data.get("status_code")

        if pages := kwargs.get("pages"):
            self.pages = pages
        else:
            if self.show_unavailable_domains:
                num_matches = resp_data.get('num_matches')
            elif domain := kwargs.get("domain"):
                num_matches = resp_data.get('num_filtered_matches')
            else:
                num_matches = resp_data.get('num_matches', 0) - resp_data.get('num_unavailable_matches', 0)
            total_pages = int(-1 * num_matches // 10 * -1)

            params = {
                'tags': kwargs.get("tags", ""),
                'show_unavailable_domains': True if self.show_unavailable_domains else '',
                'domain': kwargs.get("domain", ""),
                'sort': kwargs.get("sort", "score"),
                'order': kwargs.get("order", "desc"),
                'page': 1
            }

            filtered_params = {k: v for k, v in params.items() if v}
            base_url = f'https://tineye.com/api/v1/result_json/{self.query_hash}'
            self.pages = []
            for i in range(1, total_pages + 1):
                filtered_params['page'] = i
                self.pages.append(base_url + '?' + '&'.join(f'{k}={v}' for k, v in filtered_params.items()))


        self.page_number: int = kwargs.get("page_number", 1)
        matches = resp_data.get('matches')
        self.raw: list[TineyeItem] = [TineyeItem(i) for i in matches] if matches else []