from pathlib2 import Path
from typing import List

from ..network import HandOver


class SauceNAONorm(HandOver):
    def __init__(self, data: dict, **requests_kwargs):
        super().__init__(**requests_kwargs)
        result_header = data["header"]
        result_data = data["data"]
        self.raw: dict = data
        self.origin: dict = data
        """原始值"""
        self.similarity: float = float(result_header["similarity"])
        """相似度"""
        self.thumbnail: str = result_header["thumbnail"]
        """缩略图地址"""
        self.index_id: int = result_header["index_id"]
        """文件id"""
        self.index_name: str = result_header["index_name"]
        """文件名称"""
        self.title: str = self._get_title(result_data)
        """标题"""
        self.url: str = self._get_url(result_data)
        """url地址"""
        self.author: str = self._get_author(result_data)
        """作者"""
        self.pixiv_id: str = self._get_pixiv_id(result_data)
        """pixiv的id（如果有）"""
        self.member_id: str = self._get_member_id(result_data)
        """pixiv的画师id（如果有）"""

    async def download_thumbnail(
        self, filename="thumbnail.png", path: Path = Path.cwd()
    ) -> Path:
        """
        下载缩略图

        :param filename: 重命名文件
        :param path: 本地地址(默认当前目录)
        :return: 文件路径
        """
        endpoint = await self.downloader(self.thumbnail, path, filename)
        return endpoint

    @staticmethod
    def _get_title(data):
        if "title" in data:
            return data["title"]
        elif "eng_name" in data:
            return data["eng_name"]
        elif "material" in data:
            return data["material"]
        elif "source" in data:
            return data["source"]
        elif "created_at" in data:
            return data["created_at"]

    @staticmethod
    def _get_url(data):
        if "ext_urls" in data:
            return data["ext_urls"][0]
        elif "getchu_id" in data:
            return f'https://www.getchu.com/soft.phtml?id={data["getchu_id"]}'
        return ""

    @staticmethod
    def _get_author(data):
        if "author" in data:
            return data["author"]
        elif "author_name" in data:
            return data["author_name"]
        elif "member_name" in data:
            return data["member_name"]
        elif "pawoo_user_username" in data:
            return data["pawoo_user_username"]
        elif "company" in data:
            return data["company"]
        elif "creator" in data:
            if isinstance(data["creator"], list):
                return data["creator"][0]
            return data["creator"]

    @staticmethod
    def _get_pixiv_id(data):
        if "pixiv_id" in data:
            return data["pixiv_id"]
        else:
            return ""

    @staticmethod
    def _get_member_id(data):
        if "member_id" in data:
            return data["member_id"]
        else:
            return ""

    def __repr__(self):
        return f"<NormSauceNAO(title={repr(self.title)}, similarity={self.similarity:.2f})>"


class SauceNAOResponse:
    def __init__(self, res: dict):
        resp_header = res["header"]
        resp_results = res["results"]
        self.raw: List[SauceNAONorm] = [SauceNAONorm(i) for i in resp_results]
        """所有的返回结果"""
        self.origin: dict = res
        """原始返回结果"""
        self.short_remaining: int = resp_header["short_remaining"]  # 每30秒访问额度
        """每30秒访问额度"""
        self.long_remaining: int = resp_header["long_remaining"]  # 每天访问额度
        """每天访问额度"""
        self.user_id: int = resp_header["user_id"]
        self.account_type: int = resp_header["account_type"]
        self.short_limit: str = resp_header["short_limit"]
        self.long_limit: str = resp_header["long_limit"]
        self.status: int = resp_header["status"]
        """返回http状态值"""
        self.results_requested: int = resp_header["results_requested"]
        """数据返回值数量"""
        self.search_depth: str = resp_header["search_depth"]
        """搜索所涉及的数据库数量"""
        self.minimum_similarity: float = resp_header["minimum_similarity"]
        """最小相似度"""
        self.results_returned: int = resp_header["results_returned"]
        """数据返回值数量"""

    def __repr__(self):
        return (
            f"<SauceNAOResponse(count={repr(len(self.raw))}, long_remaining={repr(self.long_remaining)}, "
            f"short_remaining={repr(self.short_remaining)})>"
        )
