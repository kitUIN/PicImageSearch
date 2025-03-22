from re import compile
from typing import Any, Optional

from pyquery import PyQuery
from typing_extensions import override

from ..exceptions import ParsingError
from ..utils import parse_html
from .base import BaseSearchItem, BaseSearchResponse


class GoogleItem(BaseSearchItem):
    """Represents a single Google search result item.

    A class that processes and stores individual search result data from Google reverse image search.

    Attributes:
        origin (PyQuery): The raw PyQuery object containing the search result data.
        title (str): The title text of the search result.
        url (str): The URL link to the search result page.
        thumbnail (Optional[str]): Base64 encoded thumbnail image, if available.
        content (str): Descriptive text or context surrounding the image.
    """

    def __init__(self, data: PyQuery, thumbnail: Optional[str]):
        """Initializes a GoogleItem with data from a search result.

        Args:
            data (PyQuery): A PyQuery instance containing the search result item's data.
            thumbnail (Optional[str]): Optional base64 encoded thumbnail image.
        """
        super().__init__(data, thumbnail=thumbnail)

    @override
    def _parse_data(self, data: PyQuery, **kwargs: Any) -> None:
        """Parse search result data."""
        self.title: str = data("h3").text()
        self.url: str = data("a").eq(0).attr("href")
        self.thumbnail: str = kwargs.get("thumbnail") or ""
        self.content: str = data("div.VwiC3b").text()


class GoogleResponse(BaseSearchResponse[GoogleItem]):
    """Encapsulates a Google reverse image search response.

    Processes and stores the complete response from a Google reverse image search,
    including pagination information and individual search results.

    Attributes:
        origin (PyQuery): The raw PyQuery object containing the full response data.
        page_number (int): Current page number in the search results.
        url (str): URL of the current search result page.
        pages (list[str]): List of URLs for all available result pages.
        raw (list[GoogleItem]): List of processed search result items.
    """

    def __init__(
        self,
        resp_data: str,
        resp_url: str,
        page_number: int = 1,
        pages: Optional[list[str]] = None,
    ):
        """Initializes with the response text and URL.

        Args:
            resp_data (str): The text of the response.
            resp_url (str): URL to the search result page.
            page_number (int): The current page number in the search results.
            pages (Optional[list[str]]): List of URLs to pages of search results.
        """
        super().__init__(resp_data, resp_url, page_number=page_number, pages=pages)

    @override
    def _parse_response(self, resp_data: str, **kwargs: Any) -> None:
        """Parse search response data."""
        data = parse_html(resp_data)
        self.origin: PyQuery = data
        self.page_number: int = kwargs["page_number"]

        if pages := kwargs.get("pages"):
            self.pages: list[str] = pages
        else:
            self.pages = [f"https://www.google.com{i.attr('href')}" for i in data.find('a[aria-label~="Page"]').items()]
            self.pages.insert(0, kwargs["resp_url"])

        script_list = list(data.find("script").items())
        thumbnail_dict: dict[str, str] = self.create_thumbnail_dict(script_list)

        search_items = data.find("#search .wHYlTd")
        self.raw: list[GoogleItem] = [
            GoogleItem(i, thumbnail_dict.get(i('img[id^="dimg_"]').attr("id"))) for i in search_items.items()
        ]

        if thumbnail_dict and not self.raw:
            raise ParsingError(
                message="Failed to extract search results despite finding thumbnails",
                engine="google",
                details="This usually indicates a change in the page structure.",
            )

    @staticmethod
    def create_thumbnail_dict(script_list: list[PyQuery]) -> dict[str, str]:
        """Creates a mapping of image IDs to their base64 encoded thumbnails.

        Processes script tags from Google's search results to extract thumbnail images
        and their corresponding IDs.

        Args:
            script_list (list[PyQuery]): List of PyQuery objects containing script elements
                from the search results page.

        Returns:
            dict[str, str]: A dictionary where:
                - Keys are image IDs (format: 'dimg_*')
                - Values are base64 encoded image strings

        Note:
            - Handles multiple image formats (jpeg, jpg, png, gif)
            - Automatically fixes escaped base64 strings by replacing '\x3d' with '='
        """
        thumbnail_dict = {}
        base_64_regex = compile(r"data:image/(?:jpeg|jpg|png|gif);base64,[^'\"]+")
        id_regex = compile(r"dimg_[^'\"]+")

        for script in script_list:
            base_64_match = base_64_regex.findall(script.text())
            if not base_64_match:
                continue

            # extract and adjust base64 encoded thumbnails
            base64: str = base_64_match[0]
            id_list: list[str] = id_regex.findall(script.text())

            for _id in id_list:
                thumbnail_dict[_id] = base64.replace(r"\x3d", "=")

        return thumbnail_dict
