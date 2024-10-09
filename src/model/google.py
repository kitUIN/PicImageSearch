from re import compile
from typing import Any, Optional

from pyquery import PyQuery

from ..utils import parse_html
from .base import BaseSearchItem, BaseSearchResponse


class GoogleItem(BaseSearchItem):
    """Represents a single Google search result item.

    Holds details of a result from a Google reverse image search.

    Attributes:
        origin: The raw data of the search result item.
        title: Title of the search result.
        url: URL to the search result.
        thumbnail: Optional base64 encoded thumbnail image.
    """

    def __init__(self, data: PyQuery, thumbnail: Optional[str]):
        """Initializes a GoogleItem with data from a search result.

        Args:
            data: A PyQuery instance containing the search result item's data.
            thumbnail: Optional base64 encoded thumbnail image.
        """
        super().__init__(data, thumbnail=thumbnail)

    def _parse_data(self, data: PyQuery, **kwargs) -> None:
        """Parse search result data."""
        self.title: str = data("h3").text()
        self.url: str = data("a").eq(0).attr("href")
        self.thumbnail: Optional[str] = kwargs.get("thumbnail")


class GoogleResponse(BaseSearchResponse):
    """Encapsulates a Google reverse image search response.

    Contains the complete response from a Google reverse image search operation.

    Attributes:
        origin: The raw response data.
        page_number: The current page number in the search results.
        url: URL to the search result page.
        pages: List of URLs to pages of search results.
        raw: List of GoogleItem instances for each search result.
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
            resp_data: The text of the response.
            resp_url: URL to the search result page.
            page_number: The current page number in the search results.
            pages: List of URLs to pages of search results.
        """
        super().__init__(resp_data, resp_url, page_number=page_number, pages=pages)

    def _parse_response(self, resp_data: str, **kwargs: Any) -> None:
        """Parse search response data."""
        data = parse_html(resp_data)
        self.origin: PyQuery = data
        self.page_number: int = kwargs.get("page_number")

        if pages := kwargs.get("pages"):
            self.pages: list[str] = pages
        else:
            self.pages = [
                f'https://www.google.com{i.attr("href")}'
                for i in data.find('a[aria-label~="Page"]').items()
            ]
            self.pages.insert(0, kwargs.get("resp_url"))

        script_list = list(data.find("script").items())
        thumbnail_dict: dict[str, str] = self.create_thumbnail_dict(script_list)
        self.raw: list[GoogleItem] = [
            GoogleItem(i, thumbnail_dict.get(i('img[id^="dimg_"]').attr("id")))
            for i in data.find("#search .g").items()
        ]

    @staticmethod
    def create_thumbnail_dict(script_list: list[PyQuery]) -> dict[str, str]:
        """Extracts a dictionary of thumbnail images from the list of script tags.

        Parses script tags to extract a mapping of image IDs to their base64 encoded thumbnails.

        Args:
            script_list: A list of PyQuery objects each containing a script element.

        Returns:
            A dictionary where keys are image IDs and values are base64 encoded images.
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
