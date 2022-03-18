from pathlib2 import Path
from typing import List, Optional

import httpx

from ..network import HandOver


class TraceMoeAnilist:
    def __init__(self, data):
        self.id: int = data["id"]
        """匹配的Anilist ID见https://anilist.co/"""
        self.idMal: int = data["idMal"]
        """匹配的MyAnimelist ID见https://myanimelist.net/"""
        self.title: dict = data["title"]
        """番剧名字"""
        self.title_native: str = data["title"]["native"]
        """番剧国际命名"""
        self.title_english: str = data["title"]["english"]
        """番剧英文命名"""
        self.title_romaji: str = data["title"]["romaji"]
        """番剧罗马命名"""
        self.title_chinese: str = "NULL"
        """番剧中文命名"""
        self.synonyms: list = data["synonyms"]
        """备用英文标题"""
        self.isAdult: bool = data["isAdult"]
        """是否R18"""

    def set_chinese(self, data):
        self.title = data
        if "chinese" in data.keys():
            self.title_chinese: str = data["chinese"]  # 番剧中文命名

    def __repr__(self):
        return (
            f"(<id={repr(self.id)}, idMal={repr(self.idMal)}, title={repr(self.title)},"
            f" synonyms={repr(self.synonyms)}, isAdult={repr(self.isAdult)})> "
        )


class TraceMoeMe:
    def __init__(self, data):
        self.id: str = data["id"]
        """IP 地址（访客）或电子邮件地址（用户）"""
        self.priority: int = data["priority"]
        """优先级"""
        self.concurrency: int = data["concurrency"]
        """搜索请求数量"""
        self.quota: int = data["quota"]
        """本月的搜索配额"""
        self.quotaUsed: int = data["quotaUsed"]
        """本月已经使用的搜索配额"""

    def __repr__(self):
        return f"<TraceMoeMe(id={repr(len(self.id))}, quota={repr(self.quota)})>"


class TraceMoeNorm(HandOver):
    def __init__(
        self, data, chinese_title=True, mute=False, size=None, **requests_kwargs
    ):
        """

        :param data: 数据
        :param chinese_title: 中文番剧名称显示
        :param mute: 预览视频静音
        :param size: 视频与图片大小(s/m/l)
        """
        super().__init__(**requests_kwargs)
        self.origin: dict = data
        """原始数据"""
        self.idMal: int = 0
        """匹配的MyAnimelist ID见https://myanimelist.net/"""
        self.title: dict = {}
        """剧名字"""
        self.title_native: str = "NULL"
        """番剧国际命名"""
        self.title_english: str = "NULL"
        """剧英文命名"""
        self.title_romaji: str = "NULL"
        """番剧罗马命名"""
        self.title_chinese: str = "NULL"
        """番剧中文命名"""
        self.anilist: Optional[int] = None
        """匹配的Anilist ID见https://anilist.co/"""
        self.synonyms: list = []
        """备用英文标题"""
        self.isAdult: bool = False
        """是否R18"""
        if type(data["anilist"]) == dict:
            self.anilist = data["anilist"]["id"]  # 匹配的Anilist ID见https://anilist.co/
            self.idMal: int = data["anilist"][
                "idMal"
            ]  # 匹配的MyAnimelist ID见https://myanimelist.net/
            self.title: dict = data["anilist"]["title"]  # 番剧名字
            self.title_native: str = data["anilist"]["title"]["native"]  # 番剧国际命名
            self.title_english: str = data["anilist"]["title"]["english"]  # 番剧英文命名
            self.title_romaji: str = data["anilist"]["title"]["romaji"]  # 番剧罗马命名
            self.synonyms: list = data["anilist"]["synonyms"]  # 备用英文标题
            self.isAdult: bool = data["anilist"]["isAdult"]  # 是否R18
            if chinese_title:
                self.title_chinese: str = self._get_chinese_title()  # 番剧中文命名
        else:
            self.anilist = data["anilist"]  # 匹配的Anilist ID见https://anilist.co/
        self.filename: str = data["filename"]
        """找到匹配项的文件名"""
        self.episode: int = data["episode"]
        """估计的匹配的番剧的集数"""
        self.From: int = data["from"]
        """匹配场景的开始时间"""
        self.To: int = data["to"]
        """匹配场景的结束时间"""
        self.similarity: float = float(data["similarity"])
        """相似度，相似性低于 87% 的搜索结果可能是不正确的结果"""
        self.video: str = data["video"]
        """预览视频"""
        self.image: str = data["image"]
        """预览图像"""
        if size in ["l", "s", "m"]:  # 大小设置
            self.video += "&size=" + size
            self.image += "&size=" + size
        if mute:  # 视频静音设置
            self.video += "&mute"

        # ---------------过时版本-----------------------
        # self.anilist_id: int = data['anilist_id']
        # self.at: int = data['at']  # 匹配场景的确切时间
        # self.season: str = data['season']  # 发布时间
        # self.anime: str = data['anime']  # 番剧名字
        # self.tokenthumb: str = data['tokenthumb']  # 用于生成预览的token
        # self.title_native: str = data['title_native']  # 番剧世界命名
        # self.title_chinese: str = data['title_chinese']  # 番剧中文命名
        # self.title_english: str = data['title_english']  # 番剧英文命名
        # self.title_romaji: str = data['title_romaji']  # 番剧罗马命名
        # self.synonyms_chinese: list = data['synonyms_chinese']  # 备用中文标题
        # self.thumbnail: str = self._preview_image()
        # self.video_thumbnail: str = self._preview_video(mute)

    # ---------------过时版本-----------------------
    # def _preview_image(self):  # 图片预览图
    #     # parse.quote()用于网页转码
    #     url = "https://trace.moe/thumbnail.php" \
    #           "?anilist_id={}&file={}&t={}&token={}".format(self.anilist_id, parse.quote(self.filename), self.at,
    #                                                         self.tokenthumb)
    #     return url

    # def _preview_video(self, mute=False):
    #     """
    #     创建预览视频
    #     :param mute:预览视频是否静音，True为静音
    #     :return: 预览视频url地址
    #     """
    #     url = "https://media.trace.moe/video/" \
    #           f"{self.anilist_id}/{parse.quote(self.filename)}?t={self.at}&token={self.tokenthumb}"
    #         if mute:
    #            url = url + '&mute'
    #     return url

    async def download_image(
        self, filename="image.png", path: Path = Path.cwd()
    ) -> Path:
        """
        下载缩略图

        :param filename: 重命名文件
        :param path: 本地地址(默认当前目录)
        :return: 文件路径
        """
        endpoint = await self.downloader(self.image, path, filename)
        return endpoint

    async def download_video(
        self, filename="video.mp4", path: Path = Path.cwd()
    ) -> Path:
        """

        下载预览视频

        :param filename: 重命名文件
        :param path: 本地地址(默认当前目录)
        :return: 文件路径
        """
        endpoint = await self.downloader(self.video, path, filename)
        return endpoint

    def _get_chinese_title(self):
        return self.get_anime_title(self.origin["anilist"]["id"])["data"]["Media"][
            "title"
        ]["chinese"]

    @staticmethod
    def get_anime_title(anilist_id: int) -> dict:
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

    def __repr__(self):
        return f"<TraceMoeNorm(filename={repr(self.filename)}, similarity={self.similarity:.2f})>"


class TraceMoeResponse:
    def __init__(self, res, chinese_title, mute, size, **requests_kwargs):
        self.requests_kwargs = requests_kwargs
        self.origin: dict = res
        """原始数据"""
        self.raw: List[TraceMoeNorm] = list()
        """结果返回值"""
        resp_docs = res["result"]
        for i in resp_docs:
            self.raw.append(
                TraceMoeNorm(
                    i,
                    chinese_title=chinese_title,
                    mute=mute,
                    size=size,
                    **self.requests_kwargs,
                )
            )
        self.count: int = len(self.raw)
        """搜索结果数量"""
        self.frameCount: int = res["frameCount"]
        """搜索的帧总数"""
        self.error: str = res["error"]
        """错误报告"""
        # ---------------过时版本-----------------------
        # self.RawDocsSearchTime: int = res['RawDocsSearchTime']  # 从数据库检索帧所用的时间
        # self.ReRankSearchTime: int = res['ReRankSearchTime']  # 比较帧所用的时间
        # self.CacheHit: bool = res['CacheHit']  # 是否缓存搜索结果
        # self.trial: int = res['trial']  # 搜索时间
        # self.limit: int = res['limit']  # 剩余搜索限制数
        # self.limit_ttl: int = res['limit_ttl']  # 限制重置之前的时间（秒）
        # self.quota: int = res['quota']  # 剩余搜索配额数
        # self.quota_ttl: int = res['quota_ttl']  # 配额重置之前的时间（秒）

    def __repr__(self):
        return f"<TraceMoeResponse(count={repr(len(self.raw))}, frameCount={repr(self.frameCount)}"
