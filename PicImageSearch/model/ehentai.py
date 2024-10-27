from typing import Any

from pyquery import PyQuery

from ..utils import parse_html
from .base import BaseSearchItem, BaseSearchResponse


class EHentaiItem(BaseSearchItem):
    """Represents a single e-hentai gallery item from search results.

    Attributes:
        origin (PyQuery): The raw PyQuery data of the search result item.
        thumbnail (str): URL of the gallery's thumbnail image.
        url (str): Direct URL to the gallery page.
        title (str): Title of the gallery.
        type (str): Category/type of the gallery (e.g., 'Doujinshi', 'Manga', etc.).
        date (str): Upload date of the gallery.
        tags (list[str]): List of tags associated with the gallery.
    """

    def __init__(self, data: PyQuery, **kwargs: Any):
        """Initializes an EHentaiItem with data from a search result.

        Args:
            data: A PyQuery instance containing the search result item's data.
        """
        super().__init__(data, **kwargs)

    def _parse_data(self, data: PyQuery, **kwargs) -> None:
        """Initialize and parse the gallery data from search results.

        Args:
            data: PyQuery object containing the gallery's HTML data.
            **kwargs: Additional keyword arguments (unused).
        """
        self.type: str = ""
        self.date: str = ""
        self.tags: list[str] = []
        self._arrange(data)

    def _arrange(self, data: PyQuery) -> None:
        """Extract and organize gallery information from the PyQuery data.

        Processes the HTML data to extract various gallery attributes including:
        - Title and URL
        - Thumbnail image URL
        - Gallery type/category
        - Upload date
        - Associated tags

        Args:
            data: PyQuery object containing the gallery's HTML data.
        """
        glink = data.find(".glink")
        self.title = glink.text()
        if glink.parent("div"):
            self.url = glink.parent("div").parent("a").attr("href")
        else:
            self.url = glink.parent("a").attr("href")
        thumbnail = (
            data.find(".glthumb img")
            or data.find(".gl1e img")
            or data.find(".gl3t img")
        )
        self.thumbnail = thumbnail.attr("data-src") or thumbnail.attr("src")
        _type = data.find(".cs") or data.find(".cn")
        self.type = _type.eq(0).text()
        self.date = data.find("[id^='posted']").eq(0).text()
        self.tags = [
            i.attr("title") for i in data.find("div[class=gt],div[class=gtl]").items()
        ]


class EHentaiResponse(BaseSearchResponse):
    """Represents the complete response from an e-hentai reverse image search.

    This class processes and organizes the search results from e-hentai,
    handling both filtered and unfiltered results in different HTML layouts.

    Attributes:
        origin (PyQuery): The raw PyQuery data of the entire response.
        raw (list[EHentaiItem]): List of parsed gallery items from the search.
        url (str): URL of the search results page.
    """

    def __init__(self, resp_data: str, resp_url: str, **kwargs: Any):
        """Initializes with the response text and URL.

        Args:
            resp_text: The text of the response.
            resp_url: URL to the search result page.
        """
        super().__init__(resp_data, resp_url, **kwargs)

    def _parse_response(self, resp_data: str, **kwargs: Any) -> None:
        """Parse the HTML response data from e-hentai search.

        Handles different result layouts:
        - Table layout (.itg > tr)
        - Grid layout (.itg > .gl1t)
        - No results case

        Args:
            resp_data: Raw HTML string from the search response.
            **kwargs: Additional keyword arguments (unused).
        """
        data = parse_html(resp_data)
        self.origin: PyQuery = data
        if "No unfiltered results" in resp_data:
            self.raw = []
        elif tr_items := data.find(".itg").children("tr").items():
            self.raw = [EHentaiItem(i) for i in tr_items if i.children("td")]
        else:
            gl1t_items = data.find(".itg").children(".gl1t").items()
            self.raw = [EHentaiItem(i) for i in gl1t_items]
