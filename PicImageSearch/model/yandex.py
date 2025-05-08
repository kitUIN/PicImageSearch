from json import loads as json_loads
from typing import Any

from pyquery import PyQuery
from typing_extensions import override

from ..exceptions import ParsingError
from ..utils import deep_get, parse_html
from .base import BaseSearchItem, BaseSearchResponse


class YandexItem(BaseSearchItem):
    """Represents a single Yandex search result item.

    A structured representation of an individual image search result from Yandex,
    containing detailed information about the found image and its source.

    Attributes:
        url (str): Direct URL to the webpage containing the image.
        title (str): Title or heading associated with the image.
        thumbnail (str): URL of the image thumbnail, properly formatted with https if needed.
        source (str): Domain name of the website hosting the image.
        content (str): Descriptive text or context surrounding the image.
        size (str): Image dimensions in "widthxheight" format.
    """

    def __init__(self, data: dict[str, Any], **kwargs: Any):
        """Initializes a YandexItem with data from a search result.

        Args:
            data (dict[str, Any]): A dictionary containing the search result data.
        """
        super().__init__(data, **kwargs)

    @override
    def _parse_data(self, data: dict[str, Any], **kwargs: Any) -> None:
        """Parses raw search result data into structured attributes.

        Processes the raw dictionary data from Yandex and extracts relevant information
        into instance attributes.

        Args:
            data (dict[str, Any]): Dictionary containing the raw search result data from Yandex.
            **kwargs (Any): Additional keyword arguments (unused).

        Note:
            The thumbnail URL is automatically prefixed with 'https:' if it starts
            with '//' to ensure proper formatting.
        """
        self.url: str = data["url"]
        self.title: str = data["title"]
        thumb_url: str = data["thumb"]["url"]
        self.thumbnail: str = f"https:{thumb_url}" if thumb_url.startswith("//") else thumb_url
        self.source: str = data["domain"]
        self.content: str = data["description"]
        original_image = data["originalImage"]
        self.size: str = f"{original_image['width']}x{original_image['height']}"


class YandexResponse(BaseSearchResponse[YandexItem]):
    """Encapsulates a complete Yandex reverse image search response.

    Processes and stores the full response from a Yandex reverse image search,
    including all found image results and metadata.

    Attributes:
        raw (list[YandexItem]): List of parsed search results as YandexItem instances.
        url (str): URL of the search results page.
        origin (PyQuery): PyQuery object containing the raw HTML response.
    """

    def __init__(self, resp_data: str, resp_url: str, **kwargs: Any):
        """Initializes with the response text and URL.

        Args:
            resp_data (str): the text of the response.
            resp_url (str): URL to the search result page.
        """
        super().__init__(resp_data, resp_url, **kwargs)

    @override
    def _parse_response(self, resp_data: str, **kwargs: Any) -> None:
        """Parses the raw HTML response from Yandex into structured data.

        Extracts search results from the HTML response by locating and parsing
        the JSON data embedded in the page.

        Args:
            resp_data (str): Raw HTML response from Yandex search.
            **kwargs (Any): Additional keyword arguments (unused).

        Note:
            The method looks for a specific div element containing the search results
            data in JSON format, then creates YandexItem instances for each result.
        """
        data = parse_html(resp_data)
        self.origin: PyQuery = data
        data_div = data.find('div.Root[id^="ImagesApp-"]')
        data_state = data_div.attr("data-state")

        if not data_state:
            raise ParsingError(
                message="Failed to find critical DOM attribute 'data-state'",
                engine="yandex",
                details="This usually indicates a change in the page structure or an unexpected response.",
            )

        data_json = json_loads(str(data_state))
        if sites := deep_get(data_json, "initialState.cbirSites.sites"):
            self.raw: list[YandexItem] = [YandexItem(site) for site in sites]
        else:
            raise ParsingError(
                message="Failed to extract search results from 'data-state'",
                engine="yandex",
                details="This usually indicates a change in the page structure or an unexpected response.",
            )
