from re import compile
from typing import Dict, List, Optional

from lxml.html import HTMLParser, fromstring
from pyquery import PyQuery


class GoogleItem:
    """A single Google search result item.

    Attributes:
        origin: The raw data of the item.
        title: The title of the search result.
        url: The URL of the search result.
        thumbnail: The optional base64 encoded thumbnail image.
    """

    def __init__(self, data: PyQuery, thumbnail: Optional[str]):
        """Initializes a GoogleItem instance.

        Args:
            data: The PyQuery object containing the item's data.
            thumbnail: An optional base64 encoded thumbnail image.
        """
        self.origin: PyQuery = data  # 原始数据 (raw data)
        self.title: str = data("h3").text()
        self.url: str = data("a").eq(0).attr("href")
        self.thumbnail: Optional[str] = thumbnail


class GoogleResponse:
    """The response from a Google search query.

    Attributes:
        origin: The raw data of the response.
        page_number: The current page number in the search results.
        url: The URL to the Google search result page.
        pages: A list of URLs to the pages of search results.
        raw: A list of GoogleItem instances representing individual search results.
    """

    def __init__(self, resp_text: str, resp_url: str):
        """Initializes a GoogleResponse instance.

        Args:
            resp_text: The response text containing the HTML of the search results.
            resp_url: The URL from which the response was obtained.
        """
        utf8_parser = HTMLParser(encoding="utf-8")
        data = PyQuery(fromstring(resp_text, parser=utf8_parser))
        self.origin: PyQuery = data  # 原始数据 (raw data)
        self.page_number: int = 1  # 当前页 (current page)
        self.url: str = resp_url
        index = 1
        for i, item in enumerate(
            list(data.find('div[role="navigation"] td').items())[1:-1]
        ):
            if not PyQuery(item).find("a"):
                index = i + 1
                self.page_number = int(PyQuery(item).text())
                break
        self.pages: List[str] = [
            f'https://www.google.com{i.attr("href")}'
            for i in data.find('a[aria-label~="Page"]').items()
        ]
        self.pages.insert(index - 1, resp_url)
        script_list = list(data.find("script").items())
        # 结果返回值 (result returned from source)
        thumbnail_dict: Dict[str, str] = self.create_thumbnail_dict(script_list)
        self.raw: List[GoogleItem] = [
            GoogleItem(i, thumbnail_dict.get(i('img[id^="dimg_"]').attr("id")))
            for i in data.find("#search .g").items()
        ]

    @staticmethod
    def create_thumbnail_dict(script_list: List[PyQuery]) -> Dict[str, str]:
        """Extracts a dictionary of thumbnail images from the list of script tags.

        Args:
            script_list: A list of PyQuery objects each containing a script element.

        Returns:
            A dictionary where keys are image IDs and values are base64 encoded images.
        """
        thumbnail_dict = {}
        base_64_regex = compile(r"data:image/(?:jpeg|jpg|png|gif);base64,[^'\"]+")
        id_regex = compile(r"dimg_\d+")

        for script in script_list:
            base_64_match = base_64_regex.findall(script.text())
            if not base_64_match:
                continue

            base64: str = base_64_match[0]
            id_list: List[str] = id_regex.findall(script.text())

            for _id in id_list:
                thumbnail_dict[_id] = base64.replace(r"\x3d", "=")

        return thumbnail_dict
