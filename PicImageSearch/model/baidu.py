from typing import Any

from .base import BaseSearchItem, BaseSearchResponse


class BaiDuItem(BaseSearchItem):
    """Represents a single BaiDu search result item.

    Holds details of a result from a BaiDu reverse image search.

    Attributes:
        origin: The raw data of the search result item.
        thumbnail: URL of the thumbnail image.
        url: URL of the webpage with the image.
    """

    def __init__(self, data: dict[str, Any], **kwargs):
        """Initializes with data from a BaiDu search result.

        Args:
            data: A dictionary containing the search result data.
        """
        super().__init__(data, **kwargs)

    def _parse_data(self, data: dict[str, Any], **kwargs) -> None:
        """Parse search result data."""
        # deprecated attributes
        # self.similarity: float = round(float(data["simi"]) * 100, 2)
        # self.title: str = data["fromPageTitle"]
        self.thumbnail: str = data["thumbUrl"]
        self.url: str = data["fromUrl"]


class BaiDuResponse(BaseSearchResponse):
    """Encapsulates a BaiDu reverse image search response.

    Contains the complete response from a BaiDu reverse image search operation.

    Attributes:
        origin: The raw response data.
        raw: List of BaiDuItem instances for each search result.
        url: URL to the search result page.
    """

    def __init__(self, resp_data: dict[str, Any], resp_url: str, **kwargs):
        """Initializes with the JSON response and response URL.

        Args:
            resp_data: The response JSON.
            resp_url: URL to the search result page.
        """
        super().__init__(resp_data, resp_url, **kwargs)

    def _parse_response(self, resp_data: dict[str, Any], **kwargs) -> None:
        """Parse search response data."""
        self.raw: list[BaiDuItem] = (
            [BaiDuItem(i) for i in resp_data["data"]["list"]] if resp_data else []
        )
