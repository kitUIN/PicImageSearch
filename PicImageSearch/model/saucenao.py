from typing import Any, Dict, List, Optional


class SauceNAOItem:
    def __init__(self, data: Dict[str, Any]):
        result_header = data["header"]
        result_data = data["data"]
        self.origin: Dict[str, Any] = data  # 原始数据
        self.similarity: float = float(result_header["similarity"])
        self.thumbnail: str = result_header["thumbnail"]
        self.index_id: int = result_header["index_id"]  # 文件 id
        self.index_name: str = result_header["index_name"]  # 文件名称
        self.hidden: int = result_header.get("hidden", 0)  # 是否为搜索引擎参数 hide 对应的 NSFW 内容
        self.title: str = self._get_title(result_data)
        self.url: str = self._get_url(result_data)
        self.ext_urls: List[str] = result_data.get("ext_urls", [])
        self.author: str = self._get_author(result_data)
        self.author_url: str = self._get_author_url(result_data)
        self.source: str = result_data.get("source", "")

    @staticmethod
    def _get_title(data: Dict[str, Any]) -> str:
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
        return data.get("author_url", "")


class SauceNAOResponse:
    def __init__(self, data: Dict[str, Any]):
        # HTTP 状态码
        self.status_code: int = data["status_code"]
        res_header = data["header"]
        res_results = data.get("results", [])
        # 所有的返回结果
        self.raw: List[SauceNAOItem] = [SauceNAOItem(i) for i in res_results]
        self.origin: Dict[str, Any] = data  # 原始返回结果
        # 每30秒访问额度
        self.short_remaining: Optional[int] = res_header.get("short_remaining")
        # 每天访问额度
        self.long_remaining: Optional[int] = res_header.get("long_remaining")
        self.user_id: Optional[int] = res_header.get("user_id")
        self.account_type: Optional[int] = res_header.get("account_type")
        self.short_limit: Optional[str] = res_header.get("short_limit")
        self.long_limit: Optional[str] = res_header.get("long_limit")
        self.status: Optional[int] = res_header.get("status")
        # 数据返回值数量
        self.results_requested: Optional[int] = res_header.get("results_requested")
        # 搜索所涉及的数据库数量
        self.search_depth: Optional[int] = res_header.get("search_depth")
        # 最小相似度
        self.minimum_similarity: Optional[float] = res_header.get("minimum_similarity")
        # 数据返回值数量
        self.results_returned: Optional[int] = res_header.get("results_returned")
        self.url: str = (
            f"https://saucenao.com/search.php?url="
            f'https://saucenao.com{res_header.get("query_image_display")}'
        )
