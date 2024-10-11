from typing import Any, Optional
from .base import BaseSearchItem, BaseSearchResponse



class CopyseekerItem(BaseSearchItem):
    """Represents a single Copyseeker search result item.

    Holds details of a result from a Copyseeker reverse image search.

    Attributes:
        origin: The raw data of the search result item.
        url: URL of the webpage with the image.
        title: Title of the webpage.
        mainImage: URL of the main image on the page.
        otherImages: List of URLs of other images on the page.
        rank: Rank or similarity score of the result.
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
        self.mainImage: str = data.get("mainImage", "")
        self.otherImages: list[str] = data.get("otherImages", []) # Corrected type hint
        self.rank: float = data.get("rank", 0.0)



class CopyseekerResponse(BaseSearchResponse):
    """Encapsulates a Copyseeker reverse image search response.

    Contains the complete response from a Copyseeker reverse image search operation.

    Attributes:
        id: Unique identifier for the search request.
        imageUrl: URL of the image searched.
        bestGuessLabel: Copyseeker's best guess for the image category.
        entities: Entities detected in the image.
        totalLinksFound: Total number of links found.
        exif: EXIF data extracted from the image.
        raw: List of CopyseekerItem objects, each representing a search result.
        visuallySimilarImages: List of URLs of visually similar images.
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
        self.imageUrl: str = resp_data["imageUrl"]
        self.bestGuessLabel: Optional[str] = resp_data.get("bestGuessLabel")
        self.entities: Optional[str] = resp_data.get("entities")
        self.totalLinksFound: int = resp_data["totalLinksFound"]
        self.exif: dict[str, Any] = resp_data.get("exif", {})
        self.raw: list[CopyseekerItem] = [CopyseekerItem(page) for page in resp_data.get("pages", [])]
        self.visuallySimilarImages: list[str] = resp_data.get("visuallySimilarImages", [])