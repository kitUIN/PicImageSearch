from typing import Any, Dict, List


class BaiDuItem:
    """A single BaiDu search result.

    Attributes:
        origin: The raw data of the item.
        thumbnail: URL to the thumbnail image.
        url: URL to the web page where the image is located.
    """

    def __init__(self, data: Dict[str, Any]):
        """Initializes with data from a search result.

        Args:
            data: Data for the item.
        """
        self.origin: Dict[str, Any] = data  # 原始数据
        # self.similarity: float = round(float(data["simi"]) * 100, 2)  # deprecated
        # self.title: str = data["fromPageTitle"]  # 页面标题 deprecated
        self.thumbnail: str = data["thumbUrl"]  # 图片地址 (thumbnail)
        self.url: str = data["fromUrl"]  # 图片所在网页地址 (image url)


class BaiDuResponse:
    """The response from a BaiDu image search.

    Attributes:
        url: URL to the BaiDu search result page.
        origin: The raw response data.
        raw: List of BaiDuItem instances for each search result.
    """

    def __init__(self, resp_json: Dict[str, Any], resp_url: str):
        """Initializes with the JSON response and result URL.

        Args:
            resp_json: The response JSON from BaiDu.
            resp_url: URL of the search result page.
        """
        self.url: str = resp_url  # 搜索结果地址 (link to search result)
        self.origin: Dict[str, Any] = resp_json  # 原始数据 (raw data)
        # 来源结果返回值 (results returned from source)
        self.raw: List[BaiDuItem] = [BaiDuItem(i) for i in resp_json["data"]["list"]]
