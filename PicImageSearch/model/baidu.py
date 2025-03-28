from typing import Any

from typing_extensions import override

from ..utils import deep_get
from .base import BaseSearchItem, BaseSearchResponse


class BaiDuItem(BaseSearchItem):
    """Represents a single BaiDu search result item.

    A class that processes and stores individual search result data from BaiDu image search.

    Attributes:
        origin (dict): The raw, unprocessed data of the search result item.
        thumbnail (str): URL of the thumbnail image.
        url (str): URL of the webpage containing the original image.
    """

    def __init__(self, data: dict[str, Any], **kwargs: Any) -> None:
        """Initialize a BaiDu search result item.

        Args:
            data (dict[str, Any]): A dictionary containing the raw search result data from BaiDu.
            **kwargs (Any): Additional keyword arguments passed to the parent class.
        """
        super().__init__(data, **kwargs)

    @override
    def _parse_data(self, data: dict[str, Any], **kwargs: Any) -> None:
        """Parse the raw search result data into structured attributes.

        Args:
            data (dict[str, Any]): Raw dictionary data from BaiDu search result.
            **kwargs (Any): Additional keyword arguments (unused).

        Note:
            Some previously supported attributes have been deprecated:
            - similarity: Percentage of image similarity
            - title: Title of the source webpage
        """
        # deprecated attributes
        # self.similarity: float = round(float(data["simi"]) * 100, 2)
        self.title: str = deep_get(data, "title[0]") or ""
        self.thumbnail: str = data.get("image_src") or data.get("thumbUrl") or ""
        self.url: str = data.get("url") or data.get("fromUrl") or ""


class BaiDuResponse(BaseSearchResponse[BaiDuItem]):
    """Encapsulates a complete BaiDu reverse image search response.

    A class that handles and stores the full response from a BaiDu reverse image search,
    including multiple search results.

    Attributes:
        origin (dict): The complete raw response data from BaiDu.
        raw (list[BaiDuItem]): List of processed search results as BaiDuItem instances.
        exact_matches (list[BaiDuItem]): List of exact same image results as BaiDuItem instances.
        url (str): URL of the search results page on BaiDu.
    """

    def __init__(self, resp_data: dict[str, Any], resp_url: str, **kwargs: Any):
        """Initialize a BaiDu search response.

        Args:
            resp_data (dict[str, Any]): The raw JSON response from BaiDu's API.
            resp_url (str): The URL of the search results page.
            **kwargs (Any): Additional keyword arguments passed to the parent class.
        """
        super().__init__(resp_data, resp_url, **kwargs)

    @override
    def _parse_response(self, resp_data: dict[str, Any], **kwargs: Any) -> None:
        """Parse the raw response data into a list of search result items.

        Args:
            resp_data (dict[str, Any]): Raw response dictionary from BaiDu's API.
            **kwargs (Any): Additional keyword arguments (unused).

        Note:
            If resp_data is empty or invalid, an empty list will be returned.
        """
        self.raw: list[BaiDuItem] = []
        self.exact_matches: list[BaiDuItem] = []

        # Parse same image results if available
        if same_data := resp_data.get("same"):
            if "list" in same_data:
                self.exact_matches.extend(BaiDuItem(i) for i in same_data["list"] if "url" in i and "image_src" in i)

        # Parse similar image results
        if data_list := deep_get(resp_data, "data.list"):
            self.raw.extend([BaiDuItem(i) for i in data_list])
