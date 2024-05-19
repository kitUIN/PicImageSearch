from typing import Any


class BaiDuItem:
    """Represents a single BaiDu search result item.

    Holds details of a result from a BaiDu reverse image search.

    Attributes:
        origin: The raw data of the search result item.
        thumbnail: URL of the thumbnail image.
        url: URL of the webpage with the image.
    """

    def __init__(self, data: dict[str, Any]):
        """Initializes with data from a BaiDu search result.

        Args:
            data: A dictionary containing the search result data.
        """
        self.origin: dict[str, Any] = data
        # deprecated attributes
        # self.similarity: float = round(float(data["simi"]) * 100, 2)
        # self.title: str = data["fromPageTitle"]
        self.thumbnail: str = data["thumbUrl"]
        self.url: str = data["fromUrl"]


class BaiDuResponse:
    """Encapsulates a BaiDu reverse image search response.

    Contains the complete response from a BaiDu reverse image search operation.

    Attributes:
        origin: The raw response data.
        raw: List of BaiDuItem instances for each search result.
        url: URL to the search result page.
    """

    def __init__(self, resp_json: dict[str, Any], resp_url: str):
        """Initializes with the JSON response and response URL.

        Args:
            resp_json: The response JSON.
            resp_url: URL to the search result page.
        """
        self.origin: dict[str, Any] = resp_json
        self.raw: list[BaiDuItem] = (
            [BaiDuItem(i) for i in resp_json["data"]["list"]] if resp_json else []
        )
        self.url: str = resp_url
