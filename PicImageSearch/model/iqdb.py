from typing import Any

from pyquery import PyQuery
from typing_extensions import override

from ..utils import parse_html
from .base import BaseSearchItem, BaseSearchResponse


class IqdbItem(BaseSearchItem):
    """Represents a single IQDB search result item.

    Attributes:
        origin (PyQuery): The raw PyQuery data of the search result item.
        content (str): Text content describing the match type (e.g., 'Best match', 'Additional match').
        url (str): URL of the webpage containing the matched image.
        source (str): Primary source platform name where the image was found.
        other_source (list[dict[str, str]]): Additional sources, each containing 'source' name and 'url'.
        thumbnail (str): URL of the result's thumbnail image.
        size (str): Dimensions and file size of the matched image.
        similarity (float): Percentage similarity between the search image and result (0-100).
    """

    def __init__(self, data: PyQuery, **kwargs: Any):
        """Initializes an IqdbItem with data from a search result.

        Args:
            data (PyQuery): A PyQuery instance containing the search result item's data.
        """
        super().__init__(data, **kwargs)

    @override
    def _parse_data(self, data: PyQuery, **kwargs: Any) -> None:
        """Initialize and parse the search result data.

        Args:
            data (PyQuery): PyQuery object containing the HTML data for this result item.
            **kwargs (Any): Additional keyword arguments passed from parent class.
        """
        self.content: str = ""
        self.source: str = ""
        self.other_source: list[dict[str, str]] = []
        self.size: str = ""
        self._arrange(data)

    def _arrange(self, data: PyQuery) -> None:
        """Extract and organize search result data from HTML structure.

        Processes the HTML table rows to extract various attributes including:
        - Content description
        - Image URLs
        - Source information
        - Image size
        - Similarity percentage

        Args:
            data (PyQuery): PyQuery object containing the table structure of the result.

        Note:
            Handles special case for "No relevant matches" results.
        """
        tr_list = list(data("tr").items())
        if len(tr_list) >= 5:
            self.content = tr_list[0]("th").text()
            if self.content == "No relevant matches":
                return
            tr_list = tr_list[1:]
        self.url: str = self._get_url(tr_list[0]("td > a").attr("href"))
        self.thumbnail: str = "https://iqdb.org" + tr_list[0]("td > a > img").attr("src")
        source_list = [i.tail.strip() for i in tr_list[1]("img")]
        self.source = source_list[0]
        if other_source := tr_list[1]("td > a"):
            self.other_source.append(
                {
                    "source": source_list[1],
                    "url": self._get_url(other_source.attr("href")),
                }
            )
        self.size = tr_list[2]("td").text()
        similarity_raw = tr_list[3]("td").text()
        self.similarity: float = float(similarity_raw.removesuffix("% similarity"))

    @staticmethod
    def _get_url(url: str) -> str:
        """Convert a URL to its absolute form with proper protocol.

        Args:
            url (str): A URL string that may be protocol-relative (starting with //).

        Returns:
            str: Complete URL with 'https' protocol if necessary.

        Example:
            >>> _get_url("//example.com/image.jpg")
            "https://example.com/image.jpg"
        """
        return url if url.startswith("http") else f"https:{url}"


class IqdbResponse(BaseSearchResponse[IqdbItem]):
    """Represents a complete IQDB reverse image search response.

    Attributes:
        origin (PyQuery): Raw PyQuery data of the entire response.
        raw (list[IqdbItem]): Primary search results with high similarity.
        more (list[IqdbItem]): Additional results with lower similarity.
        saucenao_url (str): URL to search the same image on SauceNao.
        ascii2d_url (str): URL to search the same image on Ascii2D.
        google_url (str): URL to search the same image on Google Images.
        tineye_url (str): URL to search the same image on TinEye.
        url (str): URL of the original IQDB search results page.
    """

    def __init__(self, resp_data: str, resp_url: str, **kwargs: Any):
        """Initializes with the response text.

        Args:
            resp_data (str): The text of the response.
            resp_url (str): URL to the search result page.
        """
        super().__init__(resp_data, resp_url, **kwargs)

    @override
    def _parse_response(self, resp_data: str, **kwargs: Any) -> None:
        """Initialize and parse the complete search response.

        Args:
            resp_data (str): Raw HTML response string from IQDB.
            **kwargs (Any): Additional keyword arguments passed from parent class.
        """
        data = parse_html(resp_data)
        self.origin: PyQuery = data
        self.raw: list[IqdbItem] = []
        self.more: list[IqdbItem] = []
        self.saucenao_url: str = ""
        self.ascii2d_url: str = ""
        self.google_url: str = ""
        self.tineye_url: str = ""
        self._arrange(data)

    def _arrange(self, data: PyQuery) -> None:
        """Process and organize the complete search response data.

        Handles the following tasks:
        - Determines the correct IQDB host (regular or 3D)
        - Extracts the original search image URL
        - Processes primary search results
        - Collects URLs for other search engines
        - Handles cases with no relevant matches

        Args:
            data (PyQuery): PyQuery object containing the complete search response.
        """
        host = "https://iqdb.org" if data('a[href^="//3d.iqdb.org"]') else "https://3d.iqdb.org"
        tables = list(data("#pages > div > table").items())
        self.url: str = f"{host}/?url=https://iqdb.org{tables[0].find('img').attr('src')}"
        if len(tables) > 1:
            tables = tables[1:]
            self.raw.extend([IqdbItem(i) for i in tables])
        if tables[0].find("th").text() == "No relevant matches":
            self._get_other_urls(tables[0].find("a"))
        else:
            self._get_other_urls(data("#show1 > a"))
        self._get_more(data("#more1 > div.pages > div > table"))

    def _get_more(self, data: PyQuery) -> None:
        """Extract additional lower-similarity search results.

        Args:
            data (PyQuery): PyQuery object containing the 'more results' section.
        """
        self.more.extend([IqdbItem(i) for i in data.items()])

    def _get_other_urls(self, data: PyQuery) -> None:
        """Extract URLs for searching the image on other platforms.

        Processes links to other search engines and stores their URLs in corresponding attributes.
        Handles protocol-relative URLs by adding 'https:' prefix when needed.

        Args:
            data (PyQuery): PyQuery object containing the external search links.

        Note:
            Supports links to SauceNao, ascii2d.net, Google Images, and TinEye.
        """
        urls_with_name = {
            "SauceNao": ["https:", "saucenao"],
            "ascii2d.net": ["", "ascii2d"],
            "Google Images": ["https:", "google"],
            "TinEye": ["https:", "tineye"],
        }

        for link in data.items():
            href = link.attr("href")
            text = link.text()

            if href == "#":
                continue

            if text in urls_with_name:
                prefix, attr_name = urls_with_name[text]
                # Check if the href already contains the `https:` prefix
                full_url = href if href.startswith("https:") else prefix + href
                setattr(self, f"{attr_name}_url", full_url)
