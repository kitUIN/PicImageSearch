from typing import Any, Optional

from typing_extensions import override

from .base import BaseSearchItem, BaseSearchResponse


class CopyseekerItem(BaseSearchItem):
    """Represents a single Copyseeker search result item.

    A structured representation of an individual search result from Copyseeker's API.

    Attributes:
        origin (dict): The raw, unprocessed data of the search result.
        url (str): Direct URL to the webpage containing the matched image.
        title (str): Title of the webpage where the image was found.
        thumbnail (str): URL of the main thumbnail image.
        thumbnail_list (list[str]): List of URLs for additional related thumbnail images.
        website_rank (float): Numerical ranking score of the website (0.0 to 1.0).
    """

    def __init__(self, data: dict[str, Any], **kwargs: Any):
        """Initializes a CopyseekerItem with data from a search result.

        Args:
            data (dict[str, Any]): A dictionary containing the search result data.
        """
        super().__init__(data, **kwargs)

    @override
    def _parse_data(self, data: dict[str, Any], **kwargs: Any) -> None:
        self.url: str = data["url"]
        self.title: str = data["title"]
        self.thumbnail: str = data.get("mainImage", "")
        self.thumbnail_list: list[str] = data.get("otherImages", [])
        self.website_rank: float = data.get("rank", 0.0)


class CopyseekerResponse(BaseSearchResponse[CopyseekerItem]):
    """Encapsulates a complete Copyseeker reverse image search response.

    Provides a structured interface to access and analyze the search results
    and metadata returned by Copyseeker's API.

    Attributes:
        id (str): Unique identifier for this search request.
        image_url (str): URL of the image that was searched.
        best_guess_label (Optional[str]): AI-generated label describing the image content.
        entities (Optional[str]): Detected objects or concepts in the image.
        total (int): Total number of matching results found.
        exif (dict[str, Any]): EXIF metadata extracted from the searched image.
        raw (list[CopyseekerItem]): List of individual search results, each as a CopyseekerItem.
        similar_image_urls (list[str]): URLs of visually similar images found.
        url (str): URL to view these search results on Copyseeker's website.

    Note:
        - The 'raw' attribute contains the detailed search results, each parsed into
            a CopyseekerItem object for easier access.
        - EXIF data is only available when searching with an actual image file,
            not when searching with an image URL.
    """

    def __init__(self, resp_data: dict[str, Any], resp_url: str, **kwargs: Any) -> None:
        """Initializes with the response data.

        Args:
            resp_data (dict[str, Any]): A dictionary containing the parsed response data from Copyseeker.
            resp_url (str): URL to the search result page.
        """
        super().__init__(resp_data, resp_url, **kwargs)

    @override
    def _parse_response(self, resp_data: dict[str, Any], **kwargs: Any) -> None:
        """Parse search response data."""
        self.id: str = resp_data["id"]
        self.image_url: str = resp_data["imageUrl"]
        self.best_guess_label: Optional[str] = resp_data.get("bestGuessLabel")
        self.entities: Optional[str] = resp_data.get("entities")
        self.total: int = resp_data["totalLinksFound"]
        self.exif: dict[str, Any] = resp_data.get("exif", {})
        self.raw: list[CopyseekerItem] = [CopyseekerItem(page) for page in resp_data.get("pages", [])]
        self.similar_image_urls: list[str] = resp_data.get("visuallySimilarImages", [])
