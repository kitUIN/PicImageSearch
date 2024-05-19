from re import compile
from typing import Optional

from lxml.html import HTMLParser, fromstring
from pyquery import PyQuery


class GoogleItem:
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
        self.origin: PyQuery = data
        self.title: str = data("h3").text()
        self.url: str = data("a").eq(0).attr("href")
        self.thumbnail: Optional[str] = thumbnail


class GoogleResponse:
    """Encapsulates a Google reverse image search response.

    Contains the complete response from a Google reverse image search operation.

    Attributes:
        origin: The raw response data.
        page_number: The current page number in the search results.
        url: URL to the search result page.
        pages: List of URLs to pages of search results.
        raw: List of GoogleItem instances for each search result.
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
        self.page_number: int = 1
        self.url: str = resp_url
        index = 1
        for i, item in enumerate(
            list(data.find('div[role="navigation"] td').items())[1:-1]
        ):
            if not PyQuery(item).find("a"):
                index = i + 1
                self.page_number = int(PyQuery(item).text())
                break
        self.pages: list[str] = [
            f'https://www.google.com{i.attr("href")}'
            for i in data.find('a[aria-label~="Page"]').items()
        ]
        self.pages.insert(index - 1, resp_url)
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
        id_regex = compile(r"dimg_\d+")

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
