from typing import Dict, List

from lxml.html import HTMLParser, fromstring
from pyquery import PyQuery


class IqdbItem:
    """A single IQDB search result item.

    Attributes:
        origin: The original PyQuery object containing the item data.
        content: Text content of the result (e.g., 'Best match', 'Additional match').
        url: URL of the image provided as search result.
        source: The name of the source platform where the image was found.
        other_source (list[dict[str, str]]): A list of dictionaries containing 'source' and 'url' for
         additional sources.
        thumbnail: URL of the image's thumbnail.
        size: The dimensions and size of the image found.
        similarity: The percentage similarity between the search image and the result.

    """

    def __init__(self, data: PyQuery):
        """Initializes an IqdbItem with data from IQDB search result.

        Args:
            data: A PyQuery object representing a search result item.
        """
        self.origin: PyQuery = data  # 原始数据 (raw data)
        self.content: str = ""  # 备注
        self.url: str = ""
        self.source: str = ""  # 来源平台名称 (source platform name)
        self.other_source: List[Dict[str, str]] = []  # 其他来源数据 (data from other sources)
        self.thumbnail: str = ""
        self.size: str = ""  # 原图长宽大小 (original image width, height, size)
        self.similarity: float = 0  # 相似值
        self._arrange(data)

    def _arrange(self, data: PyQuery) -> None:
        """Arranges the PyQuery data into the object's attributes.

        Args:
            data: A PyQuery object representing a search result item.
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
    """Encapsulates the response from an IQDB image search.

    Attributes:
        origin: The original PyQuery object containing the search result data.
        raw: A list of IqdbItem objects representing the search results.
        more: A list of IqdbItem objects representing the additional search results.
        saucenao_url: URL of the search results on SauceNao.
        ascii2d_url: URL of the search results on Ascii2D.
        google_url: URL of the search results on Google Images.
        tineye_url: URL of the search results on TinEye.
        url: URL of the search results on IQDB.
    """

    def __init__(self, resp_text: str):
        """Initializes an IqdbResponse with data from IQDB search result.

        Args:
            resp_text: The HTML text of the IQDB search result.
        """
        utf8_parser = HTMLParser(encoding="utf-8")
        data = PyQuery(fromstring(resp_text, parser=utf8_parser))
        self.origin: PyQuery = data  # 原始数据 (raw data)
        self.raw: List[IqdbItem] = []  # 结果返回值 (result returned from source)
        self.more: List[
            IqdbItem
        ] = []  # 更多结果返回值 ( 低相似度)  (more results returned from source)
        self.saucenao_url: str = ""  # SauceNao 搜索链接 (SauceNao search link)
        self.ascii2d_url: str = ""  # Ascii2d 搜索链接 (Ascii2d search link)
        self.google_url: str = ""  # Google 搜索链接 (Google search link)
        self.tineye_url: str = ""  # TinEye 搜索链接 (TinEye search link)
        self.url: str = ""
        self._arrange(data)

    def _arrange(self, data: PyQuery) -> None:
        """Arranges the PyQuery data into the object's attributes.

        Args:
            data: A PyQuery object representing a search result item.
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

        Args:
            data: A PyQuery object representing a search result item.
        """
        self.more.extend([IqdbItem(i) for i in data.items()])

    def _get_other_urls(self, data: PyQuery) -> None:
        """Get URLs for other search engines.

        Args:
            data: A PyQuery object representing a search result item.
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
                # 检查 href 是否已包含 `https:` 前缀
                # check if the href already contains the `https:` prefix
                full_url = href if href.startswith("https:") else prefix + href
                setattr(self, f"{attr_name}_url", full_url)
