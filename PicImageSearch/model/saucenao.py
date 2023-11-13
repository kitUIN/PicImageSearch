from typing import Any, Dict, List, Optional


class SauceNAOItem:
    """A single search result from the SauceNAO image search engine.

    Attributes:
        origin: The original response data for the item.
        similarity: The similarity score of the search result to the query image.
        thumbnail: The URL to the thumbnail image of the search result.
        index_id: The index number of the result source on SauceNAO.
        index_name: The name of the result source index.
        hidden: An integer indicating if NSFW content is present and should be hidden (0 or 1).
        title: The title of the work associated with the image.
        url: The direct URL to the work (when available).
        ext_urls: A list of external URLs for additional information or resources related to the image.
        author: The author/creator/name of the user responsible for the work.
        author_url: The URL to the profile or page of the author/creator.
        source: The specific source of the search result, as a string.
    """

    def __init__(self, data: Dict[str, Any]):
        """Initializes a SauceNAOItem with data parsed from the SauceNAO API response.

        Args:
            data: A dictionary containing the parsed response data for an individual result.
        """
        result_header = data["header"]
        result_data = data["data"]
        self.origin: Dict[str, Any] = data  # 原始数据 (raw data)
        self.similarity: float = float(result_header["similarity"])
        self.thumbnail: str = result_header["thumbnail"]
        self.index_id: int = result_header["index_id"]  # 文件 id (file id)
        self.index_name: str = result_header["index_name"]  # 文件名称 (file name)
        self.hidden: int = result_header.get(
            "hidden", 0
        )  # 是否为搜索引擎参数 hide 对应的 NSFW 内容 (whether to hide NSFW content)
        self.title: str = self._get_title(result_data)
        self.url: str = self._get_url(result_data)
        self.ext_urls: List[str] = result_data.get("ext_urls", [])
        self.author: str = self._get_author(result_data)
        self.author_url: str = self._get_author_url(result_data)
        self.source: str = result_data.get("source", "")

    @staticmethod
    def _get_title(data: Dict[str, Any]) -> str:
        """Extracts the title from result data.

        Args:
            data: A dictionary containing the parsed data for an individual result.

        Returns:
            The title of the work as derived from the result data.
        """
        return (
            next(
                (
                    data[i]
                    for i in [
                        "title",
                        "material",
                        "jp_name",
                        "eng_name",
                        "source",
                        "created_at",
                    ]
                    if i in data and data[i]
                ),
                "",
            )
            or ""
        )

    @staticmethod
    def _get_url(data: Dict[str, Any]) -> str:
        """Constructs the URL to the work using the result data.

        Args:
            data: A dictionary containing the parsed data for an individual result.

        Returns:
            The URL to the work referenced in the search result.
        """
        if "pixiv_id" in data:
            return f'https://www.pixiv.net/artworks/{data["pixiv_id"]}'
        elif "pawoo_id" in data:
            return f'https://pawoo.net/@{data["pawoo_user_acct"]}/{data["pawoo_id"]}'
        elif "getchu_id" in data:
            return f'https://www.getchu.com/soft.phtml?id={data["getchu_id"]}'
        elif "ext_urls" in data:
            return data["ext_urls"][0]  # type: ignore
        return ""

    @staticmethod
    def _get_author(data: Dict[str, Any]) -> str:
        """Extracts the author information from the result data.

        Args:
            data: A dictionary containing the parsed data for an individual result.

        Returns:
            The name of the author or the user handle associated with the work.
        """
        return (
            next(
                (
                    ", ".join(data[i])
                    if i == "creator" and isinstance(data[i], list)
                    else data[i]
                    for i in [
                        "author",
                        "member_name",
                        "creator",
                        "twitter_user_handle",
                        "pawoo_user_display_name",
                        "author_name",
                        "user_name",
                        "artist",
                        "company",
                    ]
                    if i in data and data[i]
                ),
                "",
            )
            or ""
        )

    @staticmethod
    def _get_author_url(data: Dict[str, Any]) -> str:
        """Constructs the URL to the author's profile or page using the result data.

        Args:
            data: A dictionary containing the parsed data for an individual result.

        Returns:
            The URL to the author's profile or related page.
        """
        if "pixiv_id" in data:
            return f'https://www.pixiv.net/users/{data["member_id"]}'
        elif "seiga_id" in data:
            return f'https://seiga.nicovideo.jp/user/illust/{data["member_id"]}'
        elif "nijie_id" in data:
            return f'https://nijie.info/members.php?id={data["member_id"]}'
        elif "bcy_id" in data:
            return f'https://bcy.net/u/{data["member_id"]}'
        elif "tweet_id" in data:
            return f'https://twitter.com/intent/user?user_id={data["twitter_user_id"]}'
        elif "pawoo_user_acct" in data:
            return f'https://pawoo.net/@{data["pawoo_user_acct"]}'
        return str(data.get("author_url", ""))


class SauceNAOResponse:
    """Encapsulates the overall response from a SauceNAO image search.

    Attributes:
        status_code: The HTTP status code received from SauceNAO.
        raw: A list of SauceNAOItem instances representing individual search results.
        origin: The original response data received from the SauceNAO API.
        short_remaining: The number of search queries remaining for the short term limit.
        long_remaining: The number of search queries remaining for the daily limit.
        user_id: The user ID associated with the SauceNAO API account used.
        account_type: The type of account associated with the SauceNAO API account used.
        short_limit: Short term limit for search queries as stated by SauceNAO.
        long_limit: Daily limit for search queries as stated by SauceNAO.
        status: An integer status of the search query operation.
        results_requested: The number of results requested in the search query.
        search_depth: The number of database indexes searched by SauceNAO.
        minimum_similarity: The minimum similarity score required for results.
        results_returned: The number of results actually returned in the search response.
        url: The URL of the SauceNAO search query.
    """

    def __init__(self, data: Dict[str, Any]):
        """Initializes a SauceNAOResponse with data parsed from the SauceNAO API response.

        Args:
            data: A dictionary containing the parsed response data from SauceNAO.
        """
        # HTTP 状态码 (HTTP status code)
        self.status_code: int = data["status_code"]
        res_header = data["header"]
        res_results = data.get("results", [])
        # 所有的返回结果 (results returned from source)
        self.raw: List[SauceNAOItem] = [SauceNAOItem(i) for i in res_results]
        self.origin: Dict[str, Any] = data  # 原始返回结果
        # 每30秒访问额度 (access limit every 30 seconds)
        self.short_remaining: Optional[int] = res_header.get("short_remaining")
        # 每天访问额度 (access limit every day)
        self.long_remaining: Optional[int] = res_header.get("long_remaining")
        self.user_id: Optional[int] = res_header.get("user_id")
        self.account_type: Optional[int] = res_header.get("account_type")
        self.short_limit: Optional[str] = res_header.get("short_limit")
        self.long_limit: Optional[str] = res_header.get("long_limit")
        self.status: Optional[int] = res_header.get("status")
        # 数据返回值数量 (result returned from source)
        self.results_requested: Optional[int] = res_header.get("results_requested")
        # 搜索所涉及的数据库数量 (number of searched database indexes)
        self.search_depth: Optional[int] = res_header.get("search_depth")
        # 最小相似度 (minimum similarity)
        self.minimum_similarity: Optional[float] = res_header.get("minimum_similarity")
        # 数据返回值数量 (result returned from source)
        self.results_returned: Optional[int] = res_header.get("results_returned")
        self.url: str = (
            f"https://saucenao.com/search.php?url="
            f'https://saucenao.com{res_header.get("query_image_display")}'
        )
