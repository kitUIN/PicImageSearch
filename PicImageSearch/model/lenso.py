from typing import Any, List, Optional

from .base import BaseSearchItem, BaseSearchResponse


class LensoURLItem:
    """Represents a URL item in Lenso search results."""
    def __init__(self, data: dict[str, Any]):
        self.image_url: str = data.get("imageUrl", "")
        self.source_url: str = data.get("sourceUrl", "")
        self.title: Optional[str] = data.get("title")
        self.lang: Optional[str] = data.get("lang")


class LensoResultItem(BaseSearchItem):
    """Represents a single Lenso search result item."""

    def __init__(self, data: dict[str, Any], **kwargs: Any):
        super().__init__(data, **kwargs)

    def _parse_data(self, data: dict[str, Any], **kwargs: Any) -> None:
        self.hash: str = data.get("hash", "")
        self.similarity: float = data.get("distance", 0.0)
        self.image_proxy_url: str = data.get("proxyUrl", "")
        self.url_list: List[LensoURLItem] = [LensoURLItem(url_data) for url_data in data.get("urlList", [])]
        self.width: int = data.get("width", 0)
        self.height: int = data.get("height", 0)


class LensoResponse(BaseSearchResponse[LensoResultItem]):
    """Encapsulates a complete Lenso search response.

    Attributes:
        origin (dict): The raw JSON response data from Lenso.
        raw (List[LensoResultItem]): List of LensoResultItem objects, each representing a search result.
        url (str): URL of the search results page (API endpoint).
        similar (List[LensoResultItem]): List of similar image results.
        duplicates (List[LensoResultItem]): List of duplicate image results.
        places (List[LensoResultItem]): List of place recognition results.
        related (List[LensoResultItem]): List of related image results.
        people (List[LensoResultItem]): List of people recognition results (if applicable).
        detected_faces (List[Any]): List of detected faces (if face detection is enabled).
    """

    def __init__(self, resp_data: dict[str, Any], resp_url: str, **kwargs: Any):
        super().__init__(resp_data, resp_url, **kwargs)

    def _parse_response(self, resp_data: dict[str, Any], **kwargs: Any) -> None:
        self.raw: List[LensoResultItem] = []
        self.similar: List[LensoResultItem] = []
        self.duplicates: List[LensoResultItem] = []
        self.places: List[LensoResultItem] = []
        self.related: List[LensoResultItem] = []
        self.people: List[LensoResultItem] = []
        self.detected_faces: List[Any] = resp_data.get("detectedFaces", [])

        results_data = resp_data.get("results", {})
        self.similar = [LensoResultItem(item, type="similar") for item in results_data.get("similar", [])]
        self.duplicates = [LensoResultItem(item, type="duplicates") for item in results_data.get("duplicates", [])]
        self.places = [LensoResultItem(item, type="places") for item in results_data.get("places", [])]
        self.related = [LensoResultItem(item, type="related") for item in results_data.get("related", [])]
        self.people = [LensoResultItem(item, type="people") for item in results_data.get("people", [])]

        self.raw.extend(self.similar)
        self.raw.extend(self.duplicates)
        self.raw.extend(self.places)
        self.raw.extend(self.related)
        self.raw.extend(self.people)
