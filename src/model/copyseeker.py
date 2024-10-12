from typing import Any, Optional

from .base import BaseSearchItem, BaseSearchResponse


class CopyseekerItem(BaseSearchItem):
    """Represents a single Copyseeker search result item.

    Holds details of a result from a Copyseeker reverse image search.

    Attributes:
        origin: The raw data of the search result item.
        url: URL of the webpage with the image.
        title: Title of the webpage.
        thumbnail: URL of the thumbnail image.
        thumbnail_list: List of URLs of thumbnail images.
        website_rank: Website rank of the result.
    """

    def __init__(self, data: dict[str, Any], **kwargs: Any):
        """Initializes a CopyseekerItem with data from a search result.

        Args:
            data: A dictionary containing the search result data.
        """
        super().__init__(data, **kwargs)

    def _parse_data(self, data: dict[str, Any], **kwargs) -> None:

        self.url: str = data["url"]
        self.title: str = data["title"]
        self.thumbnail: str = data.get("mainImage", "")
        self.thumbnail_list: list[str] = data.get("otherImages", [])
        self.website_rank: float = data.get("rank", 0.0)


class CopyseekerResponse(BaseSearchResponse):
    """Encapsulates a Copyseeker reverse image search response.

    Contains the complete response from a Copyseeker reverse image search operation.

    Attributes:
        id: Unique identifier for the search request.
        image_url: URL of the image searched.
        best_guess_label: Copyseeker's best guess for the image category.
        entities: Entities detected in the image.
        total: Total number of links found.
        exif: EXIF data extracted from the image.
        raw: List of CopyseekerItem objects, each representing a search result.
        similar_image_urls: List of URLs of visually similar images.
        url: URL of the Copyseeker search results page.
    """

    def __init__(self, resp_data: dict[str, Any], resp_url: str, **kwargs):
        """Initializes with the response data.

        Args:
            resp_data: A dictionary containing the parsed response data from Copyseeker.
            resp_url: URL to the search result page.
        """
        super().__init__(resp_data, resp_url, **kwargs)

    def _parse_response(self, resp_data: dict[str, Any], **kwargs) -> None:
        """Parse search response data."""
        self.id: str = resp_data["id"]
        self.image_url: str = resp_data["imageUrl"]
        self.best_guess_label: Optional[str] = resp_data.get("bestGuessLabel")
        self.entities: Optional[str] = resp_data.get("entities")
        self.total: int = resp_data["totalLinksFound"]
        self.exif: dict[str, Any] = resp_data.get("exif", {})
        self.raw: list[CopyseekerItem] = [
            CopyseekerItem(page) for page in resp_data.get("pages", [])
        ]
        self.similar_image_urls: list[str] = resp_data.get("visuallySimilarImages", [])
