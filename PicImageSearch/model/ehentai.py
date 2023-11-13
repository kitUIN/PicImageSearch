from typing import List

from lxml.html import HTMLParser, fromstring
from pyquery import PyQuery


class EHentaiItem:
    """A single e-hentai gallery item.

    Attributes:
        origin: The raw data of the item.
        title: The title of the gallery.
        url: The URL of the gallery.
        thumbnail: The URL to the thumbnail of the gallery.
        type: The type or category of the gallery.
        date: The date when the gallery was posted.
        tags: A list of tags associated with the gallery.
    """

    def __init__(self, data: PyQuery):
        """Initializes an EHentaiItem with parsed data from a page element.

        Args:
            data: A PyQuery object containing data of the gallery item.
        """
        self.origin: PyQuery = data  # 原始数据 (raw data)
        self.title: str = ""
        self.url: str = ""
        self.thumbnail: str = ""
        self.type: str = ""
        self.date: str = ""
        self.tags: List[str] = []
        self._arrange(data)

    def _arrange(self, data: PyQuery) -> None:
        """Arranges data from a PyQuery object into attributes of the gallery item.

        Args:
            data: A PyQuery object containing data of the gallery item.
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
            i.text() for i in data.find("div[class=gt],div[class=gtl]").items()
        ]


class EHentaiResponse:
    """The response from an e-hentai gallery search.

    Attributes:
        origin: The raw data of the response.
        raw: A list of EHentaiItem instances representing gallery items.
        url: The URL to the e-hentai search result page.
    """

    def __init__(self, resp_text: str, resp_url: str):
        """Initializes an EHentaiResponse with the text response and result URL.

        Args:
            resp_text: The text of the HTTP response.
            resp_url: The URL of the search result page.
        """
        utf8_parser = HTMLParser(encoding="utf-8")
        data = PyQuery(fromstring(resp_text, parser=utf8_parser))
        self.origin: PyQuery = data  # 原始数据 (raw data)
        if "No unfiltered results found." in resp_text:
            self.raw = []
        elif tr_items := data.find(".itg").children("tr").items():
            self.raw = [EHentaiItem(i) for i in tr_items if i.children("td")]
        else:
            gl1t_items = data.find(".itg").children(".gl1t").items()
            self.raw = [EHentaiItem(i) for i in gl1t_items]
        self.url: str = resp_url
