import re
from ast import literal_eval
from typing import Any, Optional
from urllib.parse import urlparse

from pyquery import PyQuery
from typing_extensions import override

from ..utils import parse_html
from .base import BaseSearchItem, BaseSearchResponse


def get_site_name(url: Optional[str]) -> str:
    """Extracts the site name from a URL."""
    if not url:
        return ""

    parsed_url = urlparse(url)
    return parsed_url.netloc.replace("www.", "") if parsed_url.netloc else ""


def parse_image_size(html: PyQuery) -> Optional[str]:
    """Parses the image size from the HTML snippet."""
    info_spans = html("div.oYQBg.Zn52Me > span")

    for span in info_spans.items():
        text = span.text()
        if text and "x" in text:
            return text

    return None


def extract_ldi_images(script_text: str, image_url_map: dict[str, str]) -> None:
    """Extract LDI image URLs from script.

    Args:
        script_text (str): The JavaScript content to parse
        image_url_map (dict[str, str]): Dictionary to store extracted image URLs
    """
    ldi_match = re.search(r"google\.ldi\s*=\s*({[^}]+})", script_text)
    if not ldi_match:
        return

    try:
        ldi_dict = literal_eval(ldi_match[1])
        for key, value in ldi_dict.items():
            if key.startswith("dimg_"):
                image_url_map[key] = value.replace("\\u003d", "=").replace("\\u0026", "&")
    except (SyntaxError, ValueError) as e:
        print(f"Error parsing google.ldi JSON: {e}")


def extract_base64_images(script_text: str, base64_image_map: dict[str, str]) -> None:
    """Extract Base64 encoded images from script.

    Args:
        script_text (str): The JavaScript content to parse
        base64_image_map (dict[str, str]): Dictionary to store extracted base64 image data
    """
    if "_setImagesSrc" not in script_text:
        return

    image_ids_match = re.search(r"var ii=\[([^]]*)];", script_text)
    base64_match = re.search(r"var s='(data:image/[^;]+;base64,[^']+)';", script_text)

    if not (image_ids_match and base64_match):
        return

    image_ids_str = image_ids_match[1]
    image_ids = [img_id.strip().strip("'") for img_id in image_ids_str.split(",") if img_id.strip()]
    base64_str = base64_match[1]

    if image_ids and base64_str:
        for img_id in image_ids:
            base64_image_map[img_id] = base64_str


def extract_image_maps(html: PyQuery) -> tuple[dict[str, str], dict[str, str]]:
    """Extract image mapping information from HTML.

    Args:
        html (PyQuery): PyQuery object containing the page HTML

    Returns:
        tuple[dict[str, str], dict[str, str]]: A tuple containing (image_url_map, base64_image_map)
    """
    base64_image_map: dict[str, str] = {}
    image_url_map: dict[str, str] = {}

    for script_element in html("script[nonce]"):
        if script_text := PyQuery(script_element).text():
            extract_ldi_images(script_text, image_url_map)
            extract_base64_images(script_text, base64_image_map)

    return image_url_map, base64_image_map


class GoogleLensBaseItem(BaseSearchItem):
    """Base class for Google Lens items with common image extraction functionality."""

    def __init__(
        self,
        data: PyQuery,
        image_url_map: dict[str, str],
        base64_image_map: dict[str, str],
        **kwargs: Any,
    ):
        """Initializes a GoogleLensBaseItem with data and image maps.

        Args:
            data (PyQuery): PyQuery object containing the item data
            image_url_map (dict[str, str]): Dictionary mapping image IDs to URLs
            base64_image_map (dict[str, str]): Dictionary mapping image IDs to base64 data
            **kwargs (Any): Additional keyword arguments
        """
        self.image_url_map: dict[str, str] = image_url_map
        self.base64_image_map: dict[str, str] = base64_image_map
        super().__init__(data, **kwargs)

    @override
    def _parse_data(self, data: PyQuery, **kwargs: Any) -> None:
        """Parse the raw search result data.

        This method should be implemented by subclasses to extract relevant information
        from the raw data and populate the instance attributes.

        Args:
            data (PyQuery): PyQuery object containing the search result data.
            **kwargs (Any): Additional keyword arguments for specific search engines.
        """
        pass

    def _extract_image_url(self, image_element: PyQuery) -> str:
        """Extract image URL using a comprehensive approach.

        Prioritizes in this order:
        1. Maps image ID to URL from image_url_map
        2. Maps image ID to base64 data from base64_image_map
        3. Uses data-src attribute
        4. Uses src attribute

        Args:
            image_element (PyQuery): The image element to extract URL from

        Returns:
            str: The extracted image URL or empty string if not found
        """
        if not image_element:
            return ""

        # Try to get image ID from data-iid or id attribute
        if image_id := image_element.attr("data-iid") or image_element.attr("id"):
            # Check if ID exists in image URL map
            if image_id in self.image_url_map:
                return self.image_url_map[image_id]
            # Check if ID exists in base64 image map
            if image_id in self.base64_image_map:
                return self.base64_image_map[image_id]

        # Try to get from data-src attribute
        if data_src := image_element.attr("data-src"):
            return data_src

        # Try to get from src attribute
        return src if (src := image_element.attr("src")) else ""


class GoogleLensItem(GoogleLensBaseItem):
    """Represents a single Google Lens visual match item.

    Attributes:
        origin (PyQuery): The raw PyQuery object of the search result item.
        url (str): URL of the webpage containing the visual match.
        title (str): Title of the visual match result.
        site_name (str): Name of the site where the visual match is found.
        thumbnail (str): URL of the image representing the visual match.
    """

    def __init__(
        self,
        data: PyQuery,
        image_url_map: dict[str, str],
        base64_image_map: dict[str, str],
        **kwargs: Any,
    ):
        """Initializes a GoogleLensItem with data from a search result."""
        super().__init__(data, image_url_map, base64_image_map, **kwargs)

    @override
    def _parse_data(self, data: PyQuery, **kwargs: Any) -> None:
        """Parses the raw HTML data to populate item attributes."""
        link_element = data("a.LBcIee")
        title_element = data("a.LBcIee .Yt787")
        site_name_element = data("a.LBcIee .R8BTeb.q8U8x.LJEGod.du278d.i0Rdmd")
        image_element = data(".gdOPf.q07dbf.uhHOwf.ez24Df img")

        self.url: str = link_element.attr("href") if link_element else ""
        self.title: str = title_element.text() if title_element else ""

        if site_name_element:
            self.site_name: str = site_name_element.text()
        else:
            self.site_name = get_site_name(self.url)

        self.thumbnail: str = self._extract_image_url(image_element)


class GoogleLensRelatedSearchItem(GoogleLensBaseItem):
    """Represents a single Google Lens related search item.

    Attributes:
        origin (PyQuery): The raw PyQuery object of the related search item.
        url (Optional[str]): URL for the related search.
        title (str): Title of the related search suggestion.
        thumbnail (str): URL of the image associated with the related search.
    """

    def __init__(
        self,
        data: PyQuery,
        image_url_map: dict[str, str],
        base64_image_map: dict[str, str],
        **kwargs: Any,
    ):
        """Initializes a GoogleLensRelatedSearchItem with data from a related search result."""
        super().__init__(data, image_url_map, base64_image_map, **kwargs)

    @override
    def _parse_data(self, data: PyQuery, **kwargs: Any) -> None:
        """Parses the raw HTML data to populate related search item attributes."""
        url_el = data("a.Kg0xqe")
        image_element = data("img")

        if url_el and url_el.attr("href"):
            self.url: str = f"https://www.google.com{url_el.attr('href')}"

        self.title: str = data(".I9S4yc").text()
        self.thumbnail: str = self._extract_image_url(image_element)


class GoogleLensResponse(BaseSearchResponse[GoogleLensItem]):
    """Represents a complete Google Lens search response (for 'all', 'products', 'visual_matches' types).

    Attributes:
        origin (PyQuery): The raw PyQuery object of the entire response page.
        raw (list[GoogleLensItem]): List of GoogleLensItem objects representing visual matches.
        related_searches (list[GoogleLensRelatedSearchItem]): List of related search suggestions.
        url (str): URL of the search results page.
    """

    def __init__(self, resp_data: str, resp_url: str, **kwargs: Any):
        """Initializes a GoogleLensResponse with the HTML response data."""
        super().__init__(resp_data, resp_url, **kwargs)

    def _parse_search_items(
        self, html: PyQuery, image_url_map: dict[str, str], base64_image_map: dict[str, str]
    ) -> None:
        """Parse search result items from HTML.

        Args:
            html (PyQuery): PyQuery object containing the page HTML
            image_url_map (dict[str, str]): Dictionary mapping image IDs to URLs
            base64_image_map (dict[str, str]): Dictionary mapping image IDs to base64 data
        """
        items_elements = html(".vEWxFf.RCxtQc.my5z3d")
        for el in items_elements:
            item = GoogleLensItem(PyQuery(el), image_url_map, base64_image_map)
            self.raw.append(item)

    def _parse_related_searches(
        self, html: PyQuery, image_url_map: dict[str, str], base64_image_map: dict[str, str]
    ) -> None:
        """Parse related search items from HTML.

        Args:
            html (PyQuery): PyQuery object containing the page HTML
            image_url_map (dict[str, str]): Dictionary mapping image IDs to URLs
            base64_image_map (dict[str, str]): Dictionary mapping image IDs to base64 data
        """
        related_searches_elements = html(".Kg0xqe")
        for el in related_searches_elements:
            related_item = GoogleLensRelatedSearchItem(PyQuery(el), image_url_map, base64_image_map)
            self.related_searches.append(related_item)

    @override
    def _parse_response(self, resp_data: str, **kwargs: Any) -> None:
        """Parses the HTML response to extract search results and related searches."""
        html = parse_html(resp_data)
        self.origin: PyQuery = html
        self.url: str = kwargs.get("resp_url", "")
        self.raw: list[GoogleLensItem] = []
        self.related_searches: list[GoogleLensRelatedSearchItem] = []

        image_url_map, base64_image_map = extract_image_maps(html)
        self._parse_search_items(html, image_url_map, base64_image_map)
        self._parse_related_searches(html, image_url_map, base64_image_map)


class GoogleLensExactMatchesItem(GoogleLensBaseItem):
    """Represents a single Google Lens exact match item.

    Attributes:
        origin (PyQuery): The raw PyQuery object of the search result item.
        url (str): URL of the webpage containing the exact match.
        title (str): Title of the exact match result.
        site_name (str): Name of the site where the exact match is found.
        size (Optional[str]): Size information of the product, if applicable.
        thumbnail (str): URL of the image representing the exact match.
    """

    def __init__(
        self,
        data: PyQuery,
        image_url_map: dict[str, str],
        base64_image_map: dict[str, str],
        **kwargs: Any,
    ):
        """Initializes a GoogleLensExactMatchesItem with data from a search result."""
        super().__init__(data, image_url_map, base64_image_map, **kwargs)

    @override
    def _parse_data(self, data: PyQuery, **kwargs: Any) -> None:
        """Parses raw HTML to populate exact match item attributes."""
        link_element = data("a.ngTNl")
        title_element = data(".ZhosBf")
        image_element = data(".GmoL0c .zVq10e img")
        site_name_element = data(".XC18Gb .LbKnXb .xuPcX")
        info_div = data(".oYQBg.Zn52Me")

        self.url: str = link_element.attr("href") if link_element else ""
        self.title: str = title_element.text() if title_element else ""

        if site_name_element:
            self.site_name: str = site_name_element.text()
        else:
            self.site_name = get_site_name(self.url)

        self.size: Optional[str] = parse_image_size(info_div)
        self.thumbnail: str = self._extract_image_url(image_element)


class GoogleLensExactMatchesResponse(BaseSearchResponse[GoogleLensExactMatchesItem]):
    """Represents a complete Google Lens exact matches search response.

    Attributes:
        origin (PyQuery): The raw PyQuery object of the entire response page.
        raw (list[GoogleLensExactMatchesItem]): List of GoogleLensExactMatchesItem objects representing exact matches.
        url (str): URL of the search results page.
    """

    def __init__(self, resp_data: str, resp_url: str, **kwargs: Any):
        """Initializes GoogleLensExactMatchesResponse with HTML response data."""
        super().__init__(resp_data, resp_url, **kwargs)

    @staticmethod
    def _parse_search_items(
        html: PyQuery,
        image_url_map: dict[str, str],
        base64_image_map: dict[str, str],
    ) -> list[GoogleLensExactMatchesItem]:
        """Parse search result items from HTML.

        Args:
            html (PyQuery): PyQuery object containing the page HTML
            image_url_map (dict[str, str]): Dictionary mapping image IDs to URLs
            base64_image_map (dict[str, str]): Dictionary mapping image IDs to base64 data

        Returns:
            list[GoogleLensExactMatchesItem]: List of parsed exact match items
        """
        items = []
        items_elements = html(".YxbOwd")
        for el in items_elements:
            item = GoogleLensExactMatchesItem(PyQuery(el), image_url_map, base64_image_map)
            items.append(item)
        return items

    @override
    def _parse_response(self, resp_data: str, **kwargs: Any) -> None:
        """Parses HTML response to extract exact match results."""
        html = parse_html(resp_data)
        self.origin: PyQuery = html
        self.url: str = kwargs.get("resp_url", "")
        self.raw: list[GoogleLensExactMatchesItem] = []

        image_url_map, base64_image_map = extract_image_maps(html)
        self.raw = self._parse_search_items(html, image_url_map, base64_image_map)
