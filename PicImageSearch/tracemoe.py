from pathlib import Path
from typing import List, Optional

import httpx
from loguru import logger

from .Utils import get_error_message


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


class TraceMoeNorm:
    def __init__(self, data, chinese_title=True, mute=False, size=None):
        """

        :param data: 数据
        :param chinese_title: 中文番剧名称显示
        :param mute: 预览视频静音
        :param size: 视频与图片大小(s/m/l)
        """
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

    def download_image(self, filename="image.png", path: Path = Path.cwd()) -> Path:
        """
        下载缩略图

        :param path: 本地地址(默认当前目录)
        :param filename: 重命名文件
        :return: 文件路径
        """
        with httpx.stream("GET", self.image) as res:
            endpoint = path.joinpath(filename)
            with open(endpoint, "wb") as fd:
                for chunk in res.iter_bytes():
                    fd.write(chunk)
        return endpoint

    def download_video(self, filename="video.mp4", path: Path = Path.cwd()) -> Path:
        """

        下载预览视频

        :param path: 本地地址(默认当前目录)
        :param filename: 重命名文件
        :return: 文件路径
        """
        with httpx.stream("GET", self.video) as res:
            endpoint = path.joinpath(filename)
            with open(endpoint, "wb") as fd:
                for chunk in res.iter_bytes():
                    fd.write(chunk)

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

        # Make the HTTP Api request
        response = httpx.post(url, json={"query": query, "variables": variables})
        return response.json()

    def __repr__(self):
        return f"<NormTraceMoe(filename={repr(self.filename)}, similarity={self.similarity:.2f})>"


class TraceMoeResponse:
    def __init__(self, res, chinese_title, mute, size):
        self.origin: dict = res
        """原始数据"""
        self.raw: List[TraceMoeNorm] = list()
        """结果返回值"""
        resp_docs = res["result"]
        for i in resp_docs:
            self.raw.append(
                TraceMoeNorm(i, chinese_title=chinese_title, mute=mute, size=size)
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


class TraceMoeMe:
    def __init__(self, data):
        self.id: str = data["id"]  # IP 地址（访客）或电子邮件地址（用户）
        self.priority: int = data["priority"]  # 优先级
        self.concurrency: int = data["concurrency"]  # 搜索请求数量
        self.quota: int = data["quota"]  # 本月的搜索配额
        self.quotaUsed: int = data["quotaUsed"]  # 本月已经使用的搜索配额

    def __repr__(self):
        return f"<TraceMoeMe(id={repr(len(self.id))}, quota={repr(self.quota)})>"


class TraceMoe:
    search_url = "https://api.trace.moe/search"
    me_url = "https://api.trace.moe/me"

    def __init__(self, mute=False, size=None, **requests_kwargs):
        """主类

        :param size: 预览 视频/图像 大小(可填:s/m/l)(小/中/大)
        :param mute: 预览视频是否静音（默认不静音）
        :param requests_kwargs:代理设置
        """
        self.size: str = size
        self.mute: bool = mute
        self.requests_kwargs = requests_kwargs

    # @staticmethod
    # def _base_64(filename):
    #     with open(filename, 'rb') as f:
    #         coding = base64.b64encode(f.read())  # 读取文件内容，转换为base64编码
    #         # print('本地base64转码~')
    #         return coding.decode()

    def me(self, key=None) -> TraceMoeMe:  # 获取自己的信息
        try:
            params = None
            if key:
                params = {"key": key}
            res = httpx.get(self.me_url, params=params, **self.requests_kwargs)
            if res.status_code == 200:
                data = res.json()
                return TraceMoeMe(data)
            else:
                logger.error(res.status_code)
        except Exception as e:
            logger.info(e)

    @staticmethod
    def _first_if(param):
        if param != "":
            param += "&"
        return param

    @staticmethod
    def set_params(url, anilist_id, anilist_info, cut_borders):
        params = {}
        if anilist_info:
            params["anilistInfo"] = True
        if cut_borders:
            params["cutBorders"] = True
        if anilist_id:
            params["anilistID"] = anilist_id
        if url:
            params["url"] = url
        return params

    def search(
        self,
        url,
        key=None,
        anilist_id=None,
        chinese_title=True,
        anilist_info=True,
        cut_borders=True,
    ) -> TraceMoeResponse:
        """识别图片

        :param key: API密钥 https://soruly.github.io/trace.moe-api/#/limits?id=api-search-quota-and-limits
        :param url: 网络地址(http或https链接)或本地(本地图片路径)  When using video / gif, only the 1st frame would be extracted for searching.
        :param anilist_id: 搜索限制为特定的 Anilist ID(默认无)
        :param anilist_info: 详细信息(默认开启)
        :param chinese_title: 中文番剧标题
        :param cut_borders: 切割黑边框(默认开启)
        """
        try:
            headers = None
            if headers:
                headers = {"x-trace-key": key}
            if url[:4] == "http":  # 网络url
                params = self.set_params(url, anilist_id, anilist_info, cut_borders)
                res = httpx.get(
                    self.search_url,
                    headers=headers,
                    params=params,
                    verify=False,
                    **self.requests_kwargs,
                )
                if res.status_code == 200:
                    data = res.json()
                    return TraceMoeResponse(data, chinese_title, self.mute, self.size)
                else:
                    logger.error(get_error_message(res.status_code))
            else:  # 是否是本地文件
                params = self.set_params(None, anilist_id, anilist_info, cut_borders)
                res = httpx.post(
                    self.search_url,
                    headers=headers,
                    params=params,
                    files={"image": open(url, "rb")},
                    **self.requests_kwargs,
                )
                if res.status_code == 200:
                    data = res.json()
                    return TraceMoeResponse(data, chinese_title, self.mute, self.size)
                else:
                    logger.error(get_error_message(res.status_code))
        except Exception as e:
            logger.info(e)
