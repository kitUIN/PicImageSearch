import re

from typing import Any, Optional, List

from pyquery import PyQuery

from ..utils import parse_html
from .base import BaseSearchItem, BaseSearchResponse


def is_base64(url: str) -> bool:
    """Checks if a URL is a base64 encoded image (data URI)."""
    import re
    base64_pattern = r'^data:image\/(?:png|jpeg|gif|webp);base64,[A-Za-z0-9+/=]+$'
    return bool(re.match(base64_pattern, url))

def get_site_name(url: Optional[str]) -> Optional[str]:
    """Extracts the site name from a URL."""
    if not url:
        return None
    from urllib.parse import urlparse
    parsed_url = urlparse(url)
    return parsed_url.netloc.replace('www.', '') if parsed_url.netloc else None

def parse_product_info(html: PyQuery) -> dict[str, Optional[str]]:
    """Parses product information from the HTML snippet."""
    all_spans = html('div.oYQBg.Zn52Me > span')

    price = None
    size = None
    stock = None

    if len(all_spans) >= 1:
        first_span_text = all_spans.eq(0).text()
        if 'x' in first_span_text:
            size = first_span_text
        else:
            price = first_span_text

        for i in range(1, len(all_spans)):
            current_span_text = all_spans.eq(i).text()
            if 'stock' in current_span_text.lower():
                stock = current_span_text
            elif 'x' in current_span_text:
                size = current_span_text

    return {"price": price, "size": size, "stock": stock}


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
        is_base64 (bool): True if the image_url is base64 encoded, False otherwise.
    """

    def __init__(self, data: PyQuery, image_url_map: dict[str, str], base64_image_map: dict[str, str], **kwargs: Any):
        """Initializes a GoogleLensItem with data from a search result."""
        self.image_url_map = image_url_map
        self.base64_image_map = base64_image_map
        super().__init__(data, **kwargs)

    def _parse_data(self, data: PyQuery, **kwargs: Any) -> None:
        """Parses the raw HTML data to populate item attributes."""

        link_element = data('a.LBcIee')
        title_element = data('a.LBcIee .Yt787')
        site_name_element = data('a.LBcIee .R8BTeb.q8U8x.LJEGod.du278d.i0Rdmd')
        image_element = data('.gdOPf.q07dbf.uhHOwf.ez24Df img')
        stock_information_element = data('.kb0PBd .ApHyTb .h2YlCf')
        price_element = data('.nU2PHd .ALLCjc .EwVMFc')

        self.url: Optional[str] = link_element.attr('href') if link_element else None
        self.title: Optional[str] = title_element.text() if title_element else None
        self.site_name: Optional[str] = site_name_element.text() if site_name_element else get_site_name(self.url)
        self.stock_information: Optional[str] = stock_information_element.text() if stock_information_element else None
        self.price: Optional[str] = price_element.text() if price_element else None

        image_id = image_element.attr('id')
        base64_image = self.base64_image_map.get(image_id) if image_id else None
        item_image_url = base64_image if base64_image else image_element.attr('data-src')

        self.image_url: Optional[str] = item_image_url
        self.is_base64: bool = is_base64(self.image_url) if self.image_url else False


class GoogleLensRelatedSearchItem(BaseSearchItem):
    """Represents a single Google Lens related search item.

    Attributes:
        origin (PyQuery): The raw PyQuery object of the related search item.
        search_url (Optional[str]): URL for the related search.
        title (Optional[str]): Title of the related search suggestion.
        image_url (Optional[str]): URL of the image associated with the related search.
        is_base64 (bool): True if the image_url is base64 encoded, False otherwise.
    """
    def __init__(self, data: PyQuery, image_url_map: dict[str, str], base64_image_map: dict[str, str], **kwargs: Any):
        """Initializes a GoogleLensRelatedSearchItem with data from a related search result."""
        self.image_url_map = image_url_map
        self.base64_image_map = base64_image_map
        super().__init__(data, **kwargs)

    def _parse_data(self, data: PyQuery, **kwargs: Any) -> None:
        """Parses the raw HTML data to populate related search item attributes."""
        search_url_el = data('a.Kg0xqe')
        image_element = data('img')
        image_id = image_element.attr('id')

        base64_image = self.base64_image_map.get(image_id) if image_id else None
        image_url = base64_image if base64_image else image_element.attr('src')

        self.search_url: Optional[str] = "https://www.google.com" + search_url_el.attr('href') if search_url_el else None
        self.title: Optional[str] = data('.I9S4yc').text()
        self.image_url: Optional[str] = image_url
        self.is_base64: bool = is_base64(self.image_url) if self.image_url else False


class GoogleLensResponse(BaseSearchResponse[GoogleLensItem]):
    """Represents a complete Google Lens search response (for 'all', 'products', 'visual_matches' types).

    Attributes:
        origin (PyQuery): The raw PyQuery object of the entire response page.
        raw (List[GoogleLensItem]): List of GoogleLensItem objects representing visual matches.
        related_searches (List[GoogleLensRelatedSearchItem]): List of related search suggestions.
        url (str): URL of the search results page.
    """
    def __init__(self, resp_data: str, resp_url: str, **kwargs: Any):
        """Initializes a GoogleLensResponse with the HTML response data."""
        super().__init__(resp_data, resp_url, **kwargs)

    def _parse_response(self, resp_data: str, resp_url: str, **kwargs: Any) -> None:
        """Parses the HTML response to extract search results and related searches."""
        html = parse_html(resp_data)
        self.origin: PyQuery = html
        self.url: str = resp_url
        self.raw: List[GoogleLensItem] = []
        self.related_searches: List[GoogleLensRelatedSearchItem] = []

        base64_image_map = {}
        image_url_map = {}
        script_elements = html('script[nonce]')

        for script_element in script_elements:
            script_text = PyQuery(script_element).text()
            ldi_match = re.search(r'google\.ldi\s*=\s*({[^}]+})', script_text)
            if ldi_match:
                try:
                    import ast
                    ldi_dict = ast.literal_eval(ldi_match.group(1))
                    for key, value in ldi_dict.items():
                        if key.startswith("dimg_"):
                            image_url_map[key] = value.replace("\\u003d", "=").replace("\\u0026","&")
                except (SyntaxError, ValueError) as e:
                    print(f"Error parsing google.ldi JSON: {e}")
                    continue
            if "_setImagesSrc" in script_text:
                image_ids_match = re.search(r"var ii=\[([^\]]*)\];", script_text)
                base64_match = re.search(r"var s='(data:image\/jpeg;base64,[A-Za-z0-9+/]+(?:=+)?)", script_text)
                if image_ids_match and base64_match:
                    image_ids_str = image_ids_match.group(1)
                    image_ids = [img_id.strip().strip("'") for img_id in image_ids_str.split(',') if img_id.strip()]
                    base64_str = base64_match.group(1)
                    if image_ids and base64_str:
                        for img_id in image_ids:
                            base64_image_map[img_id] = base64_str


        items_elements = html('.vEWxFf.RCxtQc.my5z3d')
        for el in items_elements:
            item = GoogleLensItem(PyQuery(el), image_url_map, base64_image_map)
            self.raw.append(item)

        related_searches_elements = html('.Kg0xqe')
        for el in related_searches_elements:
            related_item = GoogleLensRelatedSearchItem(PyQuery(el), image_url_map, base64_image_map)
            self.related_searches.append(related_item)


class GoogleLensExactMatchesItem(BaseSearchItem):
    """Represents a single Google Lens exact match item.

    Attributes:
        origin (PyQuery): The raw PyQuery object of the search result item.
        url (Optional[str]): URL of the webpage containing the exact match.
        title (Optional[str]): Title of the exact match result.
        site_name (Optional[str]): Name of the site where the exact match is found.
        stock_information (Optional[str]): Stock information of the product, if applicable.
        price (Optional[str]): Price of the product, if applicable.
        size (Optional[str]): Size information of the product, if applicable.
        image_url (Optional[str]): URL of the image representing the exact match.
        is_base64 (bool): True if the image_url is base64 encoded, False otherwise.
    """
    def __init__(self, data: PyQuery, image_url_map: dict[str, str], base64_image_map: dict[str, str], **kwargs: Any):
        """Initializes a GoogleLensExactMatchesItem with data from a search result."""
        self.image_url_map = image_url_map
        self.base64_image_map = base64_image_map
        super().__init__(data, **kwargs)

    def _parse_data(self, data: PyQuery, **kwargs: Any) -> None:
        """Parses raw HTML to populate exact match item attributes."""
        link_element = data('a.ngTNl')
        title_element = data('.ZhosBf')
        image_element = data('.GmoL0c .zVq10e img')
        site_name_element = data('.XC18Gb .LbKnXb .xuPcX')
        stock_information_div = data('.oYQBg.Zn52Me')

        self.url: Optional[str] = link_element.attr('href') if link_element else None
        self.title: Optional[str] = title_element.text() if title_element else None
        self.site_name: Optional[str] = site_name_element.text() if site_name_element else get_site_name(self.url)

        product_info = parse_product_info(stock_information_div)
        self.size: Optional[str] = product_info['size']
        self.stock_information: Optional[str] = product_info['stock']
        self.price: Optional[str] = product_info['price']

        image_id = image_element.attr('data-iid') or image_element.attr('id')
        image_url = None

        if image_id:
            image_url = self.image_url_map.get(image_id)  # Try google.ldi first
            if not image_url:
                image_url = self.base64_image_map.get(image_id) # then legacy base64
            if not image_url: # then attributes
                image_url = image_element.attr('data-src')
            if not image_url:
                image_url = image_element.attr('src')
        self.image_url: Optional[str] = image_url
        self.is_base64: bool = is_base64(self.image_url) if self.image_url else False


class GoogleLensExactMatchesResponse(BaseSearchResponse[GoogleLensExactMatchesItem]):
    """Represents a complete Google Lens exact matches search response.

    Attributes:
        origin (PyQuery): The raw PyQuery object of the entire response page.
        raw (List[GoogleLensExactMatchesItem]): List of GoogleLensExactMatchesItem objects representing exact matches.
        url (str): URL of the search results page.
    """
    def __init__(self, resp_data: str, resp_url: str, **kwargs: Any):
        """Initializes GoogleLensExactMatchesResponse with HTML response data."""
        super().__init__(resp_data, resp_url, **kwargs)

    def _parse_response(self, resp_data: str, resp_url: str, **kwargs: Any) -> None:
        """Parses HTML response to extract exact match results."""
        html = parse_html(resp_data)
        self.origin: PyQuery = html
        self.url: str = resp_url
        self.raw: List[GoogleLensExactMatchesItem] = []

        base64_image_map = {}
        image_url_map = {}
        script_elements = html('script[nonce]')
        for script_element in script_elements:
            script_text = PyQuery(script_element).text()
            ldi_match = re.search(r'google\.ldi\s*=\s*({[^}]+})', script_text)
            if ldi_match:
                try:
                    import ast
                    ldi_dict = ast.literal_eval(ldi_match.group(1))
                    for key, value in ldi_dict.items():
                        if key.startswith("dimg_"):
                            image_url_map[key] = value.replace("\\u003d", "=").replace("\\u0026","&")
                except (SyntaxError, ValueError) as e:
                    print(f"Error parsing google.ldi JSON: {e}")
                    continue
            if "_setImagesSrc" in script_text:
                image_ids_match = re.search(r"var ii=\['([^']+)']", script_text)
                base64_match = re.search(r"var s='(data:image\/[^;]+;base64,[^']+)';", script_text)
                if image_ids_match and base64_match:
                    image_ids_str = image_ids_match.group(1)
                    image_ids = [img_id.strip() for img_id in image_ids_str.split(',') if img_id.strip()]
                    base64_str = base64_match.group(1)

                    if image_ids and base64_str:
                        for img_id in image_ids:
                            base64_image_map[img_id] = base64_str


        items_elements = html('.YxbOwd')
        for el in items_elements:
            item = GoogleLensExactMatchesItem(PyQuery(el), image_url_map, base64_image_map)
            self.raw.append(item)