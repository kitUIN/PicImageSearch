from typing import Any, Optional

from typing_extensions import override

from .base import BaseSearchItem, BaseSearchResponse


class SauceNAOItem(BaseSearchItem):
    """Represents a single SauceNAO search result item.

    This class processes and structures individual search results from SauceNAO,
    providing easy access to various metadata about the found image.

    Attributes:
        origin (dict): The raw JSON data of the search result.
        similarity (float): Similarity percentage between the query and result image.
        thumbnail (str): URL of the result's thumbnail image.
        index_id (int): Numerical identifier of the source database index.
        index_name (str): Human-readable name of the source database.
        hidden (int): NSFW content flag (0 for safe, non-zero for NSFW).
        title (str): Title of the artwork or content.
        url (str): Direct URL to the source content.
        ext_urls (list[str]): List of related URLs for the content.
        author (str): Creator or uploader of the content.
        author_url (str): URL to the author's profile page.
        source (str): Original source platform or website.
    """

    def __init__(self, data: dict[str, Any], **kwargs: Any):
        """Initializes a SauceNAOItem with data from a search result.

        Args:
            data (dict[str, Any]): A dictionary containing the search result data.
        """
        super().__init__(data, **kwargs)

    @override
    def _parse_data(self, data: dict[str, Any], **kwargs: Any) -> None:
        """Parse search result data."""
        header = data["header"]
        self.similarity: float = float(header["similarity"])
        self.thumbnail: str = header["thumbnail"]
        self.index_id: int = header["index_id"]
        self.index_name: str = header["index_name"]
        self.hidden: int = header.get("hidden", 0)
        self.title: str = self._get_title(data["data"])
        self.url: str = self._get_url(data["data"])
        self.ext_urls: list[str] = data["data"].get("ext_urls", [])
        self.author: str = self._get_author(data["data"])
        self.author_url: str = self._get_author_url(data["data"])
        self.source: str = data["data"].get("source", "")

    @staticmethod
    def _get_title(data: dict[str, Any]) -> str:
        """Extracts the most appropriate title from the result data.

        Attempts to find a title by checking multiple possible fields in order of preference:
        title -> material -> jp_name -> eng_name -> source -> created_at

        Args:
            data (dict[str, Any]): Dictionary containing the parsed result data.

        Returns:
            str: The most appropriate title found, or empty string if none found.
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
    def _get_url(data: dict[str, Any]) -> str:
        """Constructs the source URL based on the platform-specific identifiers.

        Handles URL generation for various platforms including:
        - Pixiv
        - Pawoo
        - Getchu
        - Generic external URLs

        Args:
            data (dict[str, Any]): Dictionary containing the parsed result data.

        Returns:
            str: The constructed URL to the source content, or empty string if no URL can be built.
        """
        if "pixiv_id" in data:
            return f"https://www.pixiv.net/artworks/{data['pixiv_id']}"
        elif "pawoo_id" in data:
            return f"https://pawoo.net/@{data['pawoo_user_acct']}/{data['pawoo_id']}"
        elif "getchu_id" in data:
            return f"https://www.getchu.com/soft.phtml?id={data['getchu_id']}"
        elif "ext_urls" in data:
            return data["ext_urls"][0]
        return ""

    @staticmethod
    def _get_author(data: dict[str, Any]) -> str:
        """Extracts the author information from multiple possible fields.

        Checks multiple fields in order of preference:
        author -> member_name -> creator -> twitter_user_handle -> pawoo_user_display_name ->
        author_name -> user_name -> artist -> company

        Args:
            data (dict[str, Any]): Dictionary containing the parsed result data.

        Returns:
            str: The author name or empty string if none found. For multiple creators,
                    returns them joined by commas.
        """
        return (
            next(
                (
                    (", ".join(data[i]) if i == "creator" and isinstance(data[i], list) else data[i])
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
    def _get_author_url(data: dict[str, Any]) -> str:
        """Constructs the author's profile URL based on the platform.

        Handles URL generation for various platforms including:
        - Pixiv
        - Nicovideo Seiga
        - Nijie
        - BCY
        - Twitter
        - Pawoo

        Args:
            data (dict[str, Any]): Dictionary containing the parsed result data.

        Returns:
            str: The constructed URL to the author's profile, or empty string if no URL can be built.
        """
        if "pixiv_id" in data:
            return f"https://www.pixiv.net/users/{data['member_id']}"
        elif "seiga_id" in data:
            return f"https://seiga.nicovideo.jp/user/illust/{data['member_id']}"
        elif "nijie_id" in data:
            return f"https://nijie.info/members.php?id={data['member_id']}"
        elif "bcy_id" in data:
            return f"https://bcy.net/u/{data['member_id']}"
        elif "tweet_id" in data:
            return f"https://twitter.com/intent/user?user_id={data['twitter_user_id']}"
        elif "pawoo_user_acct" in data:
            return f"https://pawoo.net/@{data['pawoo_user_acct']}"
        return str(data.get("author_url", ""))


class SauceNAOResponse(BaseSearchResponse[SauceNAOItem]):
    """Encapsulates a complete SauceNAO API response.

    This class processes and structures the full response from a SauceNAO search,
    including rate limit information and search results.

    Attributes:
        status_code (int): HTTP status code of the response.
        raw (list[SauceNAOItem]): List of processed search result items.
        origin (dict): The raw JSON response data.
        short_remaining (Optional[int]): Remaining queries in 30-second window.
        long_remaining (Optional[int]): Remaining queries for the day.
        user_id (Optional[int]): SauceNAO API user identifier.
        account_type (Optional[int]): Type of SauceNAO account used.
        short_limit (Optional[str]): Maximum queries allowed per 30 seconds.
        long_limit (Optional[str]): Maximum queries allowed per day.
        status (Optional[int]): API response status code.
        results_requested (Optional[int]): Number of results requested.
        search_depth (Optional[int]): Number of databases searched.
        minimum_similarity (Optional[float]): Minimum similarity threshold.
        results_returned (Optional[int]): Actual number of results returned.
        url (str): URL to view the search results on SauceNAO website.
    """

    def __init__(self, resp_data: dict[str, Any], resp_url: str, **kwargs: Any) -> None:
        """Initializes with the response data.

        Args:
            resp_data (dict[str, Any]): A dictionary containing the parsed response data from SauceNAO.
            resp_url (str): URL to the search result page.
        """
        super().__init__(resp_data, resp_url, **kwargs)

    @override
    def _parse_response(self, resp_data: dict[str, Any], **kwargs: Any) -> None:
        """Parse search response data."""
        self.status_code: int = resp_data["status_code"]
        header = resp_data["header"]
        results = resp_data.get("results", [])
        self.raw: list[SauceNAOItem] = [SauceNAOItem(i) for i in results]
        self.short_remaining: Optional[int] = header.get("short_remaining")
        self.long_remaining: Optional[int] = header.get("long_remaining")
        self.user_id: Optional[int] = header.get("user_id")
        self.account_type: Optional[int] = header.get("account_type")
        self.short_limit: Optional[str] = header.get("short_limit")
        self.long_limit: Optional[str] = header.get("long_limit")
        self.status: Optional[int] = header.get("status")
        self.results_requested: Optional[int] = header.get("results_requested")
        self.search_depth: Optional[int] = header.get("search_depth")
        self.minimum_similarity: Optional[float] = header.get("minimum_similarity")
        self.results_returned: Optional[int] = header.get("results_returned")
        self.url: str = f"https://saucenao.com/search.php?url=https://saucenao.com{header.get('query_image_display')}"
