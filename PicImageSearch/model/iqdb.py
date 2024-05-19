from lxml.html import HTMLParser, fromstring
from pyquery import PyQuery


class IqdbItem:
    """Represents a single IQDB search result item.

    Holds details of a result from an IQDB reverse image search.

    Attributes:
        origin: The raw data of the search result item.
        content: Text content of the result (e.g., 'Best match', 'Additional match').
        url: URL of the webpage with the image.
        source: Name of the source platform where the image was found.
        other_source: Additional source URLs and their corresponding source names.
        thumbnail: URL of the thumbnail image.
        size: Dimensions and size of the image found.
        similarity: Percentage similarity between the search image and the result.
    """

    def __init__(self, data: PyQuery):
        """Initializes an IqdbItem with data from a search result.

        Args:
            data: A PyQuery instance containing the search result item's data.
        """
        self.origin: PyQuery = data
        self.content: str = ""
        self.url: str = ""
        self.source: str = ""
        self.other_source: list[dict[str, str]] = []
        self.thumbnail: str = ""
        self.size: str = ""
        self.similarity: float = 0
        self._arrange(data)

    def _arrange(self, data: PyQuery) -> None:
        """Organize search result data.

        Extracts and sets the content, URL, source, other sources, thumbnail, size,
         and similarity attributes from the given data.

        Args:
            data: A PyQuery instance containing the search result item's data.
        """
        tr_list = list(data("tr").items())
        if len(tr_list) >= 5:
            self.content = tr_list[0]("th").text()
            if self.content == "No relevant matches":
                return
            tr_list = tr_list[1:]
        self.url = self._get_url(tr_list[0]("td > a").attr("href"))
        self.thumbnail = "https://iqdb.org" + tr_list[0]("td > a > img").attr("src")
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
        self.similarity = float(similarity_raw.rstrip("% similarity"))

    @staticmethod
    def _get_url(url: str) -> str:
        """Converts a potentially protocol-relative URL to an absolute URL.

        Args:
            url: A URL string that may or may not include the http(s) protocol.

        Returns:
            str: The absolute URL with 'https' prepended if necessary.
        """
        return url if url.startswith("http") else f"https:{url}"


class IqdbResponse:
    """Encapsulates an IQDB reverse image search response.

    Contains the complete response from an IQDB reverse image search operation.

    Attributes:
        origin: The raw response data.
        raw: List of IqdbItem instances for each search result.
        more: Additional IqdbItem objects for lower similarity results.
        saucenao_url: URL of the search results on SauceNao.
        ascii2d_url: URL of the search results on Ascii2D.
        google_url: URL of the search results on Google Images.
        tineye_url: URL of the search results on TinEye.
        url: URL to the original IQDB search result page.
    """

    def __init__(self, resp_text: str):
        """Initializes with the response text.

        Args:
            resp_text: The text of the response.
        """
        utf8_parser = HTMLParser(encoding="utf-8")
        data = PyQuery(fromstring(resp_text, parser=utf8_parser))
        self.origin: PyQuery = data
        self.raw: list[IqdbItem] = []
        self.more: list[IqdbItem] = []
        self.saucenao_url: str = ""
        self.ascii2d_url: str = ""
        self.google_url: str = ""
        self.tineye_url: str = ""
        self.url: str = ""
        self._arrange(data)

    def _arrange(self, data: PyQuery) -> None:
        """Arranges the PyQuery data into the object's attributes.

        Extracts and sets the search result URL, primary and additional search results,
         and URLs for other search engines.

        Args:
            data: A PyQuery instance representing a search result item.
        """
        host = (
            "https://iqdb.org"
            if data('a[href^="//3d.iqdb.org"]')
            else "https://3d.iqdb.org"
        )
        tables = list(data("#pages > div > table").items())
        self.url = f'{host}/?url=https://iqdb.org{tables[0].find("img").attr("src")}'
        if len(tables) > 1:
            tables = tables[1:]
            self.raw.extend([IqdbItem(i) for i in tables])
        if tables[0].find("th").text() == "No relevant matches":
            self._get_other_urls(tables[0].find("a"))
        else:
            self._get_other_urls(data("#show1 > a"))
        self._get_more(data("#more1 > div.pages > div > table"))

    def _get_more(self, data: PyQuery) -> None:
        """Get additional search results with lower similarity.

        Extracts additional search results from the provided data.

        Args:
            data: A PyQuery instance representing the search result item.
        """
        self.more.extend([IqdbItem(i) for i in data.items()])

    def _get_other_urls(self, data: PyQuery) -> None:
        """Get URLs for other search engines.

        Extracts and sets the URLs for searches on other platforms like SauceNao, ascii2d.net, Google Images,
         and TinEye.

        Args:
            data: A PyQuery instance representing the search result item.
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
