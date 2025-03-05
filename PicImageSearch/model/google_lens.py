import re
from typing import Any, Optional

from pyquery import PyQuery

from ..utils import parse_html
from .base import BaseSearchItem, BaseSearchResponse


def get_site_name(url: Optional[str]) -> Optional[str]:
    """Extracts the site name from a URL."""
    if not url:
        return None
    from urllib.parse import urlparse

    parsed_url = urlparse(url)
    return parsed_url.netloc.replace("www.", "") if parsed_url.netloc else None


def parse_size(html: PyQuery) -> Optional[str]:
    """Parses the size from the HTML snippet.

    Args:
        html (PyQuery): PyQuery object containing size information

    Returns:
        Optional[str]: Size information, if found.
    """
    info_spans = html("div.oYQBg.Zn52Me > span")

    for span in info_spans.items():
        text = span.text()
        if text and "x" in text:
            return text

    return None


class GoogleLensItem(BaseSearchItem):
    """Represents a single Google Lens visual match item.

    Attributes:
        origin (PyQuery): The raw PyQuery object of the search result item.
        url (Optional[str]): URL of the webpage containing the visual match.
        title (Optional[str]): Title of the visual match result.
        site_name (Optional[str]): Name of the site where the visual match is found.
        stock_information (Optional[str]): Stock information of the product, if applicable.
        price (Optional[str]): Price of the product, if applicable.
        image_url (Optional[str]): URL of the image representing the visual match.
    """

    def __init__(
        self,
        data: PyQuery,
        image_url_map: dict[str, str],
        base64_image_map: dict[str, str],
        **kwargs: Any,
    ):
        """Initializes a GoogleLensItem with data from a search result."""
        self.image_url_map = image_url_map
        self.base64_image_map = base64_image_map
        super().__init__(data, **kwargs)

    def _extract_image_url(self, image_element: PyQuery) -> Optional[str]:
        """Extract image URL, prioritize base64 encoded images, then use data-src attribute."""
        if not image_element:
            return None

        image_id = image_element.attr("id")
        if image_id and image_id in self.base64_image_map:
            return self.base64_image_map[image_id]

        return image_element.attr("data-src")

    def _parse_data(self, data: PyQuery, **kwargs: Any) -> None:
        """Parses the raw HTML data to populate item attributes."""

        link_element = data("a.LBcIee")
        title_element = data("a.LBcIee .Yt787")
        site_name_element = data("a.LBcIee .R8BTeb.q8U8x.LJEGod.du278d.i0Rdmd")
        image_element = data(".gdOPf.q07dbf.uhHOwf.ez24Df img")

        self.url: Optional[str] = link_element.attr("href") if link_element else None
        self.title: Optional[str] = title_element.text() if title_element else None
        self.site_name: Optional[str] = (
            site_name_element.text() if site_name_element else get_site_name(self.url)
        )
        self.image_url: Optional[str] = self._extract_image_url(image_element)


class GoogleLensRelatedSearchItem(BaseSearchItem):
    """Represents a single Google Lens related search item.

    Attributes:
        origin (PyQuery): The raw PyQuery object of the related search item.
        search_url (Optional[str]): URL for the related search.
        title (Optional[str]): Title of the related search suggestion.
        image_url (Optional[str]): URL of the image associated with the related search.
    """

    def __init__(
        self,
        data: PyQuery,
        image_url_map: dict[str, str],
        base64_image_map: dict[str, str],
        **kwargs: Any,
    ):
        """Initializes a GoogleLensRelatedSearchItem with data from a related search result."""
        self.image_url_map = image_url_map
        self.base64_image_map = base64_image_map
        super().__init__(data, **kwargs)

    def _extract_image_url(self, image_element: PyQuery) -> Optional[str]:
        """Extract image URL, prioritize base64 encoded images, then use data-src attribute."""
        if not image_element:
            return None

        image_id = image_element.attr("id")
        if image_id and image_id in self.base64_image_map:
            return self.base64_image_map[image_id]

        return image_element.attr("src")

    def _parse_data(self, data: PyQuery, **kwargs: Any) -> None:
        """Parses the raw HTML data to populate related search item attributes."""
        search_url_el = data("a.Kg0xqe")
        image_element = data("img")

        self.search_url: Optional[str] = (
            f"https://www.google.com{search_url_el.attr('href')}"
            if search_url_el and search_url_el.attr("href")
            else None
        )
        self.title: Optional[str] = data(".I9S4yc").text()
        self.image_url: Optional[str] = self._extract_image_url(image_element)


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

    def _extract_image_maps(self, html: PyQuery) -> dict[str, Any]:
        """Extract image mapping information."""
        base64_image_map = {}
        image_url_map = {}

        for script_element in html("script[nonce]"):
            script_text = PyQuery(script_element).text()
            self._extract_ldi_images(script_text, image_url_map)
            self._extract_base64_images(script_text, base64_image_map)

        return {"base64_map": base64_image_map, "url_map": image_url_map}

    def _extract_ldi_images(
        self, script_text: str, image_url_map: dict[str, Any]
    ) -> None:
        """Extract LDI image URLs from script."""
        ldi_match = re.search(r"google\.ldi\s*=\s*({[^}]+})", script_text)
        if not ldi_match:
            return

        try:
            import ast

            ldi_dict = ast.literal_eval(ldi_match.group(1))
            for key, value in ldi_dict.items():
                if key.startswith("dimg_"):
                    image_url_map[key] = value.replace("\\u003d", "=").replace(
                        "\\u0026", "&"
                    )
        except (SyntaxError, ValueError) as e:
            print(f"Error parsing google.ldi JSON: {e}")

    def _extract_base64_images(
        self, script_text: str, base64_image_map: dict[str, Any]
    ) -> None:
        """Extract Base64 encoded images from script."""
        if "_setImagesSrc" not in script_text:
            return

        image_ids_match = re.search(r"var ii=\[([^\]]*)\];", script_text)
        base64_match = re.search(
            r"var s='(data:image\/jpeg;base64,[A-Za-z0-9+/]+(?:=+)?)", script_text
        )

        if not (image_ids_match and base64_match):
            return

        image_ids_str = image_ids_match.group(1)
        image_ids = [
            img_id.strip().strip("'")
            for img_id in image_ids_str.split(",")
            if img_id.strip()
        ]
        base64_str = base64_match.group(1)

        if image_ids and base64_str:
            for img_id in image_ids:
                base64_image_map[img_id] = base64_str

    def _parse_search_items(self, html: PyQuery, image_maps: dict[str, Any]) -> None:
        """Parse search result items."""
        items_elements = html(".vEWxFf.RCxtQc.my5z3d")
        for el in items_elements:
            item = GoogleLensItem(
                PyQuery(el), image_maps["url_map"], image_maps["base64_map"]
            )
            self.raw.append(item)

    def _parse_related_searches(
        self, html: PyQuery, image_maps: dict[str, Any]
    ) -> None:
        """Parse related search items."""
        related_searches_elements = html(".Kg0xqe")
        for el in related_searches_elements:
            related_item = GoogleLensRelatedSearchItem(
                PyQuery(el), image_maps["url_map"], image_maps["base64_map"]
            )
            self.related_searches.append(related_item)

    def _parse_response(self, resp_data: str, resp_url: str, **kwargs: Any) -> None:
        """Parses the HTML response to extract search results and related searches."""
        html = parse_html(resp_data)
        self.origin: PyQuery = html
        self.url: str = resp_url
        self.raw: list[GoogleLensItem] = []
        self.related_searches: list[GoogleLensRelatedSearchItem] = []

        image_maps = self._extract_image_maps(html)

        self._parse_search_items(html, image_maps)
        self._parse_related_searches(html, image_maps)


class GoogleLensExactMatchesItem(BaseSearchItem):
    """Represents a single Google Lens exact match item.

    Attributes:
        origin (PyQuery): The raw PyQuery object of the search result item.
        url (Optional[str]): URL of the webpage containing the exact match.
        title (Optional[str]): Title of the exact match result.
        site_name (Optional[str]): Name of the site where the exact match is found.
        size (Optional[str]): Size information of the product, if applicable.
        image_url (Optional[str]): URL of the image representing the exact match.
    """

    def __init__(
        self,
        data: PyQuery,
        image_url_map: dict[str, str],
        base64_image_map: dict[str, str],
        **kwargs: Any,
    ):
        """Initializes a GoogleLensExactMatchesItem with data from a search result."""
        self.image_url_map = image_url_map
        self.base64_image_map = base64_image_map
        super().__init__(data, **kwargs)

    def _extract_image_url(self, image_element: PyQuery) -> Optional[str]:
        """Extract image URL, prioritize base64 encoded images, then use data-src attribute."""
        if not image_element:
            return None

        if image_id := image_element.attr("data-iid") or image_element.attr("id"):
            if image_id in self.image_url_map:
                return self.image_url_map[image_id]
            elif image_id in self.base64_image_map:
                return self.base64_image_map[image_id]
            elif image_element.attr("data-src"):
                return image_element.attr("data-src")
            elif image_element.attr("src"):
                return image_element.attr("src")

        return None

    def _parse_data(self, data: PyQuery, **kwargs: Any) -> None:
        """Parses raw HTML to populate exact match item attributes."""
        link_element = data("a.ngTNl")
        title_element = data(".ZhosBf")
        image_element = data(".GmoL0c .zVq10e img")
        site_name_element = data(".XC18Gb .LbKnXb .xuPcX")
        info_div = data(".oYQBg.Zn52Me")

        self.url: Optional[str] = link_element.attr("href") if link_element else None
        self.title: Optional[str] = title_element.text() if title_element else None
        self.site_name: Optional[str] = (
            site_name_element.text() if site_name_element else get_site_name(self.url)
        )
        self.size: Optional[str] = parse_size(info_div)
        self.image_url: Optional[str] = self._extract_image_url(image_element)


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

    def _extract_ldi_images(
        self, script_text: str, image_url_map: dict[str, Any]
    ) -> None:
        """Extract LDI image URLs from script."""
        ldi_match = re.search(r"google\.ldi\s*=\s*({[^}]+})", script_text)
        if not ldi_match:
            return

        try:
            import ast

            ldi_dict = ast.literal_eval(ldi_match.group(1))
            for key, value in ldi_dict.items():
                if key.startswith("dimg_"):
                    image_url_map[key] = value.replace("\\u003d", "=").replace(
                        "\\u0026", "&"
                    )
        except (SyntaxError, ValueError) as e:
            print(f"Error parsing google.ldi JSON: {e}")

    def _extract_base64_images(
        self, script_text: str, base64_image_map: dict[str, Any]
    ) -> None:
        """Extract Base64 encoded images from script."""
        if "_setImagesSrc" not in script_text:
            return

        image_ids_match = re.search(r"var ii=\['([^']+)']", script_text)
        base64_match = re.search(
            r"var s='(data:image\/[^;]+;base64,[^']+)';", script_text
        )

        if not (image_ids_match and base64_match):
            return

        image_ids_str = image_ids_match.group(1)
        image_ids = [
            img_id.strip() for img_id in image_ids_str.split(",") if img_id.strip()
        ]
        base64_str = base64_match.group(1)

        if image_ids and base64_str:
            for img_id in image_ids:
                base64_image_map[img_id] = base64_str

    def _extract_image_maps(
        self, html: PyQuery
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        """Extract image mapping information."""
        base64_image_map = {}
        image_url_map = {}

        for script_element in html("script[nonce]"):
            script_text = PyQuery(script_element).text()
            self._extract_ldi_images(script_text, image_url_map)
            self._extract_base64_images(script_text, base64_image_map)

        return image_url_map, base64_image_map

    def _parse_search_items(
        self,
        html: PyQuery,
        image_url_map: dict[str, Any],
        base64_image_map: dict[str, Any],
    ) -> list[GoogleLensExactMatchesItem]:
        """Parse search result items."""
        items = []
        items_elements = html(".YxbOwd")
        for el in items_elements:
            item = GoogleLensExactMatchesItem(
                PyQuery(el), image_url_map, base64_image_map
            )
            items.append(item)
        return items

    def _parse_response(self, resp_data: str, resp_url: str, **kwargs: Any) -> None:
        """Parses HTML response to extract exact match results."""
        html = parse_html(resp_data)
        self.origin: PyQuery = html
        self.url: str = resp_url
        self.raw: list[GoogleLensExactMatchesItem] = []

        image_url_map, base64_image_map = self._extract_image_maps(html)
        self.raw = self._parse_search_items(html, image_url_map, base64_image_map)
