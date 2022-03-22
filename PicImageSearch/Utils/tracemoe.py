from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import httpx

from ..network import HandOver


class TraceMoeMe:
    def __init__(self, data: Dict[str, Any]):
        self.id: str = data["id"]  # IP 地址（访客）或电子邮件地址（用户）
        self.priority: int = data["priority"]  # 优先级
        self.concurrency: int = data["concurrency"]  # 搜索请求数量
        self.quota: int = data["quota"]  # 本月的搜索配额
        self.quotaUsed: int = data["quotaUsed"]  # 本月已经使用的搜索配额


class TraceMoeNorm(HandOver):
    def __init__(
        self,
        data: Dict[str, Any],
        chinese_title: bool = True,
        mute: bool = False,
        size: Optional[str] = None,
        **requests_kwargs: Any
    ):
        """

        :param data: 数据
        :param chinese_title: 中文番剧名称显示
        :param mute: 预览视频静音
        :param size: 视频与图片大小(s/m/l)
        """
        super().__init__(**requests_kwargs)
        self.origin: Dict[str, Any] = data  # 原始数据
        self.idMal: int = 0  # 匹配的MyAnimelist ID见https://myanimelist.net/
        self.title: Dict[str, str] = {}
        self.title_native: str = ""
        """番剧国际命名"""
        self.title_english: str = ""
        self.title_romaji: str = ""
        self.title_chinese: str = ""
        self.anilist: Optional[int] = None  # 匹配的Anilist ID见https://anilist.co/
        self.synonyms: List[str] = []  # 备用英文标题
        self.isAdult: bool = False
        if type(data["anilist"]) == dict:
            self.anilist = data["anilist"]["id"]
            self.idMal = data["anilist"]["idMal"]
            self.title = data["anilist"]["title"]
            self.title_native = data["anilist"]["title"]["native"]
            self.title_english = data["anilist"]["title"]["english"]
            self.title_romaji = data["anilist"]["title"]["romaji"]
            self.synonyms = data["anilist"]["synonyms"]
            self.isAdult = data["anilist"]["isAdult"]
            if chinese_title:
                self.title_chinese = self._get_chinese_title()
        else:
            self.anilist = data["anilist"]
        self.filename: str = data["filename"]
        self.episode: int = data["episode"]
        self.From: int = data["from"]
        self.To: int = data["to"]
        self.similarity: float = float(data["similarity"]) * 100
        self.video: str = data["video"]
        self.image: str = data["image"]
        if size in ["l", "s", "m"]:  # 大小设置
            self.video += "&size=" + size
            self.image += "&size=" + size
        if mute:  # 视频静音设置
            self.video += "&mute"

    async def download_image(
        self, path: Optional[str], filename: str = "image.png"
    ) -> Path:
        """
        下载缩略图

        :param filename: 重命名文件
        :param path: 本地地址(默认当前目录)
        :return: 文件路径
        """
        endpoint = await self.downloader(self.image, filename, path)
        return endpoint

    async def download_video(
        self, path: Optional[str], filename: str = "video.mp4"
    ) -> Path:
        """

        下载预览视频

        :param filename: 重命名文件
        :param path: 本地地址(默认当前目录)
        :return: 文件路径
        """
        endpoint = await self.downloader(self.video, filename, path)
        return endpoint

    def _get_chinese_title(self) -> Union[str, Any]:
        return self.get_anime_title(self.origin["anilist"]["id"])["data"]["Media"][
            "title"
        ]["chinese"]

    @staticmethod
    def get_anime_title(anilist_id: int) -> Any:
        """获取中文标题

        :param anilist_id: id
        :return: dict
        """
        query = """
        query ($id: Int) { # Define which variables will be used in the query (id)
          Media (id: $id, type: ANIME) { # Insert our variables into the query arguments (id) (type: ANIME is hard-coded in the query)
            id
            title {
              romaji
              english
              native
            }
          }
        }
        """

        # Define our query variables and values that will be used in the query request
        variables = {"id": anilist_id}

        url = "https://trace.moe/anilist/"

        response = httpx.post(url, json={"query": query, "variables": variables})
        return response.json()


class TraceMoeResponse:
    def __init__(
        self,
        data: Dict[str, Any],
        chinese_title: bool,
        mute: bool,
        size: Optional[str],
        **requests_kwargs: Any
    ):
        self.origin: Dict[str, Any] = data  # 原始数据
        self.raw: List[TraceMoeNorm] = []  # 结果返回值
        res_docs = data["result"]
        for i in res_docs:
            self.raw.append(
                TraceMoeNorm(
                    i,
                    chinese_title=chinese_title,
                    mute=mute,
                    size=size,
                    **requests_kwargs,
                )
            )
        self.frameCount: int = data["frameCount"]  # 搜索的帧总数
        self.error: str = data["error"]  # 错误报告
