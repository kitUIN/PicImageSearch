from typing import Any, Dict, List, Optional, Union


class SauceNAOItem:
    def __init__(self, data: Dict[str, Any]):
        result_header = data["header"]
        result_data = data["data"]
        self.origin: Dict[str, Any] = data  # 原始数据
        self.similarity: float = float(result_header["similarity"])
        self.thumbnail: str = result_header["thumbnail"]
        self.index_id: int = result_header["index_id"]  # 文件 id
        self.index_name: str = result_header["index_name"]  # 文件名称
        self.title: str = self._get_title(result_data)
        self.url: str = self._get_url(result_data)
        self.author: str = self._get_author(result_data)
        self.pixiv_id: int = result_data.get("pixiv_id", 0)
        self.member_id: int = result_data.get("member_id", 0)

    @staticmethod
    def _get_title(data: Dict[str, Any]) -> Union[str, Any]:
        return next(
            (
                data[i]
                for i in [
                    "title",
                    "jp_name",
                    "eng_name",
                    "material",
                    "source",
                    "created_at",
                ]
                if i in data
            ),
            "",
        )

    @staticmethod
    def _get_url(data: Dict[str, Any]) -> Union[str, Any]:
        if "ext_urls" in data:
            return data["ext_urls"][0]
        elif "getchu_id" in data:
            return f'https://www.getchu.com/soft.phtml?id={data["getchu_id"]}'
        return ""

    @staticmethod
    def _get_author(data: Dict[str, Any]) -> Union[str, Any]:
        return next(
            (
                data[i][0] if i == "creator" and isinstance(data[i], list) else data[i]
                for i in [
                    "author",
                    "author_name",
                    "member_name",
                    "pawoo_user_username",
                    "company",
                    "creator",
                ]
                if i in data
            ),
            "",
        )


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
