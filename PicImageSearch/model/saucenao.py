from typing import Any, Dict, List, Union


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
        for i in ["title", "jp_name", "eng_name", "material", "source", "created_at"]:
            if i in data:
                return data[i]
        return ""

    @staticmethod
    def _get_url(data: Dict[str, Any]) -> Union[str, Any]:
        if "ext_urls" in data:
            return data["ext_urls"][0]
        elif "getchu_id" in data:
            return f'https://www.getchu.com/soft.phtml?id={data["getchu_id"]}'
        return ""

    @staticmethod
    def _get_author(data: Dict[str, Any]) -> Union[str, Any]:
        for i in [
            "author",
            "author_name",
            "member_name",
            "pawoo_user_username",
            "company",
            "creator",
        ]:
            if i in data:
                if i == "creator" and isinstance(data[i], list):
                    return data[i][0]
                return data[i]
        return ""


class SauceNAOResponse:
    def __init__(self, data: Dict[str, Any]):
        res_header = data["header"]
        res_results = data["results"]
        # 所有的返回结果
        self.raw: List[SauceNAOItem] = [SauceNAOItem(i) for i in res_results]
        self.origin: Dict[str, Any] = data  # 原始返回结果
        self.short_remaining: int = res_header["short_remaining"]  # 每30秒访问额度
        self.long_remaining: int = res_header["long_remaining"]  # 每天访问额度
        self.user_id: int = res_header["user_id"]
        self.account_type: int = res_header["account_type"]
        self.short_limit: str = res_header["short_limit"]
        self.long_limit: str = res_header["long_limit"]
        self.status: int = res_header["status"]  # 返回http状态值
        self.results_requested: int = res_header["results_requested"]  # 数据返回值数量
        self.search_depth: int = res_header["search_depth"]  # 搜索所涉及的数据库数量
        self.minimum_similarity: float = res_header["minimum_similarity"]  # 最小相似度
        self.results_returned: int = res_header["results_returned"]  # 数据返回值数量
