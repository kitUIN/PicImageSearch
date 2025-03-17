from typing import Any, NamedTuple

from pyquery import PyQuery
from typing_extensions import override

from ..utils import parse_html
from .base import BaseSearchItem, BaseSearchResponse

BASE_URL = "https://ascii2d.net"
SUPPORTED_SOURCES = [
    "fanbox",
    "fantia",
    "misskey",
    "pixiv",
    "twitter",
    "ニコニコ静画",
    "ニジエ",
]


class URL(NamedTuple):
    """Represents a URL in Ascii2D search results.

    Contains both the URL link and its associated display text.

    Attributes:
        href (str): The URL link address.
        text (str): The display text or description for the URL.
    """

    href: str
    text: str


class Ascii2DItem(BaseSearchItem):
    """Represents a single Ascii2D search result item.

    Holds details of a result from an Ascii2D reverse image search, including image metadata,
    URLs, author information, and related content.

    Attributes:
        origin (PyQuery): The raw PyQuery data of the search result item.
        hash (str): The hash string from the search result.
        detail (str): Image details including dimensions, type, and size.
        thumbnail (str): URL of the thumbnail image.
        url (str): Primary URL of the webpage containing the image.
        url_list (list[URL]): List of related URLs with their text descriptions.
        title (str): Title of the image or related content.
        author (str): Name of the image author/creator.
        author_url (str): URL to the author's profile page.
    """

    def __init__(self, data: PyQuery, **kwargs: Any) -> None:
        """Initializes an Ascii2DItem with data from a search result.

        Args:
            data (PyQuery): A PyQuery instance containing the search result item's data.
        """
        super().__init__(data, **kwargs)

    @override
    def _parse_data(self, data: PyQuery, **kwargs: Any) -> None:
        """Parses raw search result data into structured attributes.

        Extracts and processes various pieces of information from the PyQuery data,
        including hash, image details, thumbnail URL, and other metadata.

        Args:
            data (PyQuery): PyQuery object containing the search result HTML.
            **kwargs (Any): Additional keyword arguments (unused).
        """
        self.hash: str = data("div.hash").eq(0).text()
        self.detail: str = data("small").eq(0).text()
        image_source = data("img").eq(0).attr("src")
        self.thumbnail: str = f"{BASE_URL}{image_source}" if image_source.startswith("/") else image_source
        self.url_list: list[URL] = []
        self.author: str = ""
        self.author_url: str = ""
        self._arrange(data)

    def _arrange(self, data: PyQuery) -> None:
        """Organizes and processes the search result data.

        Coordinates the extraction of URLs, title, author information, and other metadata.
        Handles the normalization of URLs and sets backup links if necessary.

        Args:
            data (PyQuery): PyQuery object containing the detail box information.
        """
        if infos := data.find("div.detail-box.gray-link"):
            links = infos.find("a")
            self.url_list = [URL(i.attr("href"), i.text()) for i in links.items()] if links else []
            mark = next(
                (small.text() for small in infos("small").items() if small.text() in SUPPORTED_SOURCES),
                "",
            )
            self._arrange_links(infos, links, mark)
            self._arrange_title(infos)
        self._normalize_url_list()
        if not self.url_list:
            self._arrange_backup_links(data)

    def _arrange_links(self, infos: PyQuery, links: PyQuery, mark: str) -> None:
        """Processes and organizes the URLs found in the search result.

        Extracts primary URL, author URL, title, and author name based on the source type.
        Handles different link patterns based on the source platform.

        Args:
            infos (PyQuery): PyQuery object containing the detail box information.
            links (PyQuery): PyQuery object containing all URL links.
            mark (str): Source identifier string (e.g., "pixiv", "twitter").
        """
        if links:
            link_items = list(links.items())
            if len(link_items) > 1 and mark in SUPPORTED_SOURCES:
                self.title: str = link_items[0].text()
                self.url: str = link_items[0].attr("href")
                self.author_url = link_items[1].attr("href")
                self.author = link_items[1].text()
            elif links.eq(0).parents("small"):
                infos.remove("small")
                self.title = infos.text()

    def _arrange_title(self, infos: PyQuery) -> None:
        """Extracts and processes the title from the search result.

        Handles various title formats and removes unwanted text patterns.
        Falls back to external text or h6 content if primary title is not found.

        Args:
            infos (PyQuery): PyQuery object containing the title information.
        """
        if not self.title:
            self.title = self._extract_external_text(infos) or infos.find("h6").text()
        if self.title and any(i in self.title for i in {"詳細掲示板のログ", "2ちゃんねるのログ"}):
            self.title = ""

    @staticmethod
    def _extract_external_text(infos: PyQuery) -> str:
        """Extracts text from external elements in the search result.

        Removes link elements and combines remaining text content.

        Args:
            infos (PyQuery): PyQuery object containing external text elements.

        Returns:
            str: Combined text from external elements, or empty string if none found.
        """
        external = infos.find(".external")
        external.remove("a")
        return "\n".join(i.text() for i in external.items() if i.text()) or ""

    def _normalize_url_list(self) -> None:
        """Normalizes all URLs in the url_list to absolute paths.

        Converts relative URLs to absolute URLs by prepending the BASE_URL when necessary.
        Modifies the url_list attribute in place.
        """
        self.url_list = [
            URL(BASE_URL + url.href, url.text) if url.href.startswith("/") else url for url in self.url_list
        ]

    def _arrange_backup_links(self, data: PyQuery) -> None:
        """Sets backup URLs when primary URL list is empty.

        Extracts URLs from alternative locations in the HTML structure.

        Args:
            data (PyQuery): PyQuery object to search for backup links.
        """
        if links := data.find("div.pull-xs-right > a"):
            self.url = links.eq(0).attr("href")
            self.url_list = [URL(self.url, links.eq(0).text())]


class Ascii2DResponse(BaseSearchResponse[Ascii2DItem]):
    """Represents a complete Ascii2D reverse image search response.

    Processes and contains all search results from an Ascii2D search operation.

    Attributes:
        origin (PyQuery): The raw PyQuery data of the complete response.
        raw (list[Ascii2DItem]): List of processed search result items.
        url (str): URL of the search results page.
    """

    def __init__(self, resp_data: str, resp_url: str, **kwargs: Any):
        """Initializes with the response text and URL.

        Args:
            resp_data (str): The data of the response.
            resp_url (str): URL to the search result page.
        """
        super().__init__(resp_data, resp_url, **kwargs)

    @override
    def _parse_response(self, resp_data: str, **kwargs: Any) -> None:
        """Parses the raw response data into structured search results.

        Converts HTML response into PyQuery object and extracts individual search items.

        Args:
            resp_data (str): Raw HTML response string from Ascii2D.
            **kwargs (Any): Additional keyword arguments (unused).
        """
        data = parse_html(resp_data)
        self.origin: PyQuery = data
        self.raw: list[Ascii2DItem] = [Ascii2DItem(i) for i in data.find("div.row.item-box").items()]
