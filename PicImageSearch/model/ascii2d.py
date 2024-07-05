from collections import namedtuple

from lxml.html import HTMLParser, fromstring
from pyquery import PyQuery

BASE_URL = "https://ascii2d.net"
SUPPORTED_SOURCES = [
    "fanbox",
    "fantia",
    "misskey",
    "pixiv",
    "twitter",
    "げっちゅ屋",
    "ニコニコ静画",
    "ニジエ",
]
URL = namedtuple("URL", ["href", "text"])


class Ascii2DItem:
    """Represents a single Ascii2D search result item.

    Holds details of a result from an Ascii2D reverse image search.

    Attributes:
        origin: The raw data of the search result item.
        hash: The hash string from the search result.
        detail: Image details like dimensions, type, and size.
        thumbnail: URL of the thumbnail image.
        url: URL of the webpage with the image.
        url_list: List of URLs with text descriptions.
        title: Title of the image or related content.
        author: Author of the image or related content.
        author_url: URL to the author's page or profile.
    """

    def __init__(self, data: PyQuery):
        """Initializes an Ascii2DItem with data from a search result.

        Args:
            data: A PyQuery instance containing the search result item's data.
        """
        self.origin: PyQuery = data
        self.hash: str = data("div.hash").eq(0).text()
        self.detail: str = data("small").eq(0).text()
        self.thumbnail: str = BASE_URL + data("img").eq(0).attr("src")
        self.url: str = ""
        self.url_list: list[URL] = []
        self.title: str = ""
        self.author: str = ""
        self.author_url: str = ""
        self._arrange(data)

    def _arrange(self, data: PyQuery) -> None:
        """Organize search result data.

        Extracts and sets the URL list, title, author, and author URL from the provided data.

        Also normalizes the URL list and sets backup links if necessary.

        Args:
            data: A PyQuery instance containing the search result item's data.
        """
        if infos := data.find("div.detail-box.gray-link"):
            links = infos.find("a")
            self.url_list = (
                [URL(i.attr("href"), i.text()) for i in links.items()] if links else []
            )
            mark = next(
                (
                    small.text()
                    for small in infos("small").items()
                    if small.text() in SUPPORTED_SOURCES
                ),
                "",
            )
            self._arrange_links(infos, links, mark)
            self._arrange_title(infos)
        self._normalize_url_list()
        if not self.url_list:
            self._arrange_backup_links(data)

    def _arrange_links(self, infos: PyQuery, links: PyQuery, mark: str) -> None:
        """Extract and set the primary and author URLs, along with the title and author name for the search result item.

        Args:
            infos: A PyQuery instance containing additional information about the search result.
            links: A PyQuery instance containing the URL links.
            mark: A string identifier used to determine the source of the link.
        """
        if links:
            link_items = list(links.items())
            if len(link_items) > 1 and mark in SUPPORTED_SOURCES:
                self.title, self.url = link_items[0].text(), link_items[0].attr("href")
                self.author_url, self.author = (
                    link_items[1].attr("href"),
                    link_items[1].text(),
                )
            elif links.eq(0).parents("small"):
                infos.remove("small")
                self.title = infos.text()

    def _arrange_title(self, infos: PyQuery) -> None:
        """Extract and refine the title of the search result.

        The method removes certain predefined keywords from the title if they are present.

        Args:
            infos: A PyQuery instance to extract the title from.
        """
        if not self.title:
            self.title = self._extract_external_text(infos) or infos.find("h6").text()
        if self.title and any(
            i in self.title for i in {"詳細掲示板のログ", "2ちゃんねるのログ"}
        ):
            self.title = ""

    @staticmethod
    def _extract_external_text(infos: PyQuery) -> str:
        external = infos.find(".external")
        external.remove("a")
        return "\n".join(i.text() for i in external.items() if i.text()) or ""

    def _normalize_url_list(self) -> None:
        """Normalize the URL list to absolute paths."""
        self.url_list = [
            URL(BASE_URL + url.href, url.text) if url.href.startswith("/") else url
            for url in self.url_list
        ]

    def _arrange_backup_links(self, data: PyQuery) -> None:
        """Set backup links if the main URL list is empty.

        Args:
            data: A PyQuery instance to search for backup links.
        """
        if links := data.find("div.pull-xs-right > a"):
            self.url = links.eq(0).attr("href")
            self.url_list = [URL(self.url, links.eq(0).text())]


class Ascii2DResponse:
    """Encapsulates an Ascii2D reverse image search response.

    Contains the complete response from an Ascii2D reverse image search operation.

    Attributes:
        origin: The raw response data.
        raw: List of Ascii2DItem instances for each search result.
        url: URL to the search result page.
    """

    def __init__(self, resp_text: str, resp_url: str):
        """Initializes with the response text and URL.

        Args:
            resp_text: The text of the response.
            resp_url: URL to the search result page.
        """
        utf8_parser = HTMLParser(encoding="utf-8")
        data = PyQuery(fromstring(resp_text, parser=utf8_parser))
        self.origin: PyQuery = data
        self.raw: list[Ascii2DItem] = [
            Ascii2DItem(i) for i in data.find("div.row.item-box").items()
        ]
        self.url: str = resp_url
