from typing import Any

from typing_extensions import override

from ..utils import deep_get
from .base import BaseSearchItem, BaseSearchResponse


class LensoURLItem:
    """Represents a URL item in Lenso search results.

    A class that processes and stores URL-related information from a Lenso search result.

    Attributes:
        origin (dict): The raw JSON data of the URL item.
        image_url (str): Direct URL to the full-size image.
        source_url (str): URL of the webpage containing the image.
        title (str): Title or description of the image.
        lang (str): Language of the webpage.
    """

    def __init__(self, data: dict[str, Any]) -> None:
        self.origin: dict[str, Any] = data
        self.image_url: str = data.get("imageUrl", "")
        self.source_url: str = data.get("sourceUrl", "")
        self.title: str = data.get("title") or ""
        self.lang: str = data.get("lang", "")


class LensoResultItem(BaseSearchItem):
    """Represents a single Lenso search result item.

    Attributes:
        origin (dict): The raw JSON data of the search result item.
        title (str): Title or name of the search result.
        url (str): URL of the webpage containing the image.
        hash (str): The hash of the image.
        similarity (float): The similarity score (0-100).
        thumbnail (str): URL of the thumbnail version of the image.
        url_list (list[LensoURLItem]): List of related URLs.
        width (int): The width of the image.
        height (int): The height of the image.
    """

    def __init__(self, data: dict[str, Any], **kwargs: Any) -> None:
        self.url_list: list[LensoURLItem] = []
        self.width: int = 0
        self.height: int = 0
        super().__init__(data, **kwargs)

    @override
    def _parse_data(self, data: dict[str, Any], **kwargs: Any) -> None:
        """Parse search result data."""
        self.origin: dict[str, Any] = data
        self.title: str = deep_get(data, "urlList[0].title") or ""
        self.url: str = deep_get(data, "urlList[0].sourceUrl") or ""
        self.hash: str = data.get("hash", "")

        distance: float = data.get("distance", 0.0)
        self.similarity: float = round(distance * 100, 2)

        self.thumbnail: str = data.get("proxyUrl", "")
        self.url_list = [LensoURLItem(url_data) for url_data in data.get("urlList", [])]
        self.width = data.get("width", 0)
        self.height = data.get("height", 0)


class LensoResponse(BaseSearchResponse[LensoResultItem]):
    """Encapsulates a complete Lenso search response.

    Attributes:
        origin (dict): The raw JSON response data from Lenso.
        raw (list[LensoResultItem]): List of all search results.
        url (str): URL of the search results page.
        similar (list[LensoResultItem]): Similar image results.
        duplicates (list[LensoResultItem]): Duplicate image results.
        places (list[LensoResultItem]): Place recognition results.
        related (list[LensoResultItem]): Related image results.
        people (list[LensoResultItem]): People recognition results.
        detected_faces (list[Any]): Detected faces in the image.
    """

    def __init__(self, resp_data: dict[str, Any], resp_url: str, **kwargs: Any) -> None:
        """Initializes with the response data.

        Args:
            resp_data (dict[str, Any]): A dictionary containing the parsed response data from Lenso's API.
            resp_url (str): URL of the search results page.
            **kwargs (Any): Additional keyword arguments.
        """
        self.raw: list[LensoResultItem] = []
        self.duplicates: list[LensoResultItem] = []
        self.similar: list[LensoResultItem] = []
        self.places: list[LensoResultItem] = []
        self.related: list[LensoResultItem] = []
        self.people: list[LensoResultItem] = []
        self.detected_faces: list[Any] = []
        super().__init__(resp_data, resp_url, **kwargs)

    @override
    def _parse_response(self, resp_data: dict[str, Any], **kwargs: Any) -> None:
        """Parse the raw response data into structured results.

        Args:
            resp_data (dict[str, Any]): Raw response dictionary from Lenso's API.
            **kwargs (Any): Additional keyword arguments (unused).
        """
        self.detected_faces = resp_data.get("detectedFaces", [])

        results_data = resp_data.get("results", {})
        result_types = {
            "duplicates": self.duplicates,
            "similar": self.similar,
            "places": self.places,
            "related": self.related,
            "people": self.people,
        }

        for result_type, result_list in result_types.items():
            result_list.extend(LensoResultItem(item) for item in results_data.get(result_type, []))
            self.raw.extend(result_list)
