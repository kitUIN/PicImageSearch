import requests
from loguru import logger
from pathlib import Path


class TraceMoeAnilist:
    def __init__(self, data):
        self.id: int = data['id']  # 匹配的Anilist ID见https://anilist.co/
        self.idMal: int = data['idMal']  # 匹配的MyAnimelist ID见https://myanimelist.net/
        self.title: dict = data['title']  # 番剧名字
        self.synonyms: list = data['synonyms']  # 备用英文标题
        self.isAdult: bool = data['isAdult']  # 是否R18

    def __repr__(self):
        return f'(<id={repr(self.id)}, idMal={repr(self.idMal)}, title={repr(self.title)},' \
               f' synonyms={repr(self.synonyms)}, isAdult={repr(self.isAdult)})> '


class TraceMoeNorm:
    def __init__(self, data, mute=False, size=None):
        self.origin: dict = data
        if type(data['anilist']) == dict:
            self.anilist = TraceMoeAnilist(data['anilist'])
        else:
            self.anilist: int = data['anilist']  # 匹配的Anilist ID见https://anilist.co/
        self.filename: str = data['filename']  # 找到匹配项的文件名
        self.episode: int = data['episode']  # 估计的匹配的番剧的集数
        self.From: int = data['from']  # 匹配场景的开始时间
        self.To: int = data['to']  # 匹配场景的结束时间
        self.similarity: float = float(data['similarity'])  # 相似度，相似性低于 87% 的搜索结果可能是不正确的结果
        self.video: str = data['video']  # 预览视频
        self.image: str = data['image']  # 预览图像
        if size in ['l', 's', 'm']:  # 大小设置
            self.video += '&size=' + size
            self.image += '&size=' + size
        if mute:  # 视频静音设置
            self.video += '&mute'

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

    def download_image(self, filename='image.png', path: Path = Path.cwd()) -> Path:
        """
        下载缩略图

        :param path: 本地地址(默认当前目录)
        :param filename: 重命名文件
        :return: 文件路径
        """
        with requests.get(self.image, stream=True) as resp:
            endpoint = path.joinpath(filename)
            with open(endpoint, 'wb') as fd:
                for chunk in resp.iter_content():
                    fd.write(chunk)
        return endpoint

    def download_video(self, filename='video.mp4', path: Path = Path.cwd()) -> Path:
        """

        下载预览视频

        :param path: 本地地址(默认当前目录)
        :param filename: 重命名文件
        :return: 文件路径
        """
        with requests.get(self.video, stream=True) as resp:
            endpoint = path.joinpath(filename)
            with open(endpoint, 'wb') as fd:
                for chunk in resp.iter_content():
                    fd.write(chunk)

        return endpoint

    def __repr__(self):
        return f'<NormTraceMoe(filename={repr(self.filename)}, similarity={self.similarity:.2f})>'


class TraceMoeResponse:
    def __init__(self, resp, mute, size):
        self.raw: list = []
        resp_docs = resp['result']
        for i in resp_docs:
            self.raw.append(TraceMoeNorm(i, mute=mute, size=size))
        self.count: int = len(self.raw)
        self.origin: dict = resp
        self.frameCount: int = resp['frameCount']  # 搜索的帧总数
        self.error: str = resp['error']  # 错误报告
        # ---------------过时版本-----------------------
        # self.RawDocsSearchTime: int = resp['RawDocsSearchTime']  # 从数据库检索帧所用的时间
        # self.ReRankSearchTime: int = resp['ReRankSearchTime']  # 比较帧所用的时间
        # self.CacheHit: bool = resp['CacheHit']  # 是否缓存搜索结果
        # self.trial: int = resp['trial']  # 搜索时间
        # self.limit: int = resp['limit']  # 剩余搜索限制数
        # self.limit_ttl: int = resp['limit_ttl']  # 限制重置之前的时间（秒）
        # self.quota: int = resp['quota']  # 剩余搜索配额数
        # self.quota_ttl: int = resp['quota_ttl']  # 配额重置之前的时间（秒）

    def __repr__(self):
        return f'<TraceMoeResponse(count={repr(len(self.raw))}, frameCount={repr(self.frameCount)}'


class TraceMoeMe:
    def __init__(self, data):
        self.id: str = data["id"]  # IP 地址（访客）或电子邮件地址（用户）
        self.priority: int = data["priority"]  # 优先级
        self.concurrency: int = data["concurrency"]  # 搜索请求数量
        self.quota: int = data["quota"]  # 本月的搜索配额
        self.quotaUsed: int = data["quotaUsed"]  # 本月已经使用的搜索配额

    def __repr__(self):
        return f'<TraceMoeMe(id={repr(len(self.id))}, quota={repr(self.quota)})>'


class TraceMoe:
    TraceMoeURL = 'https://api.trace.moe/search'
    MeURL = 'https://api.trace.moe/me'

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

    @staticmethod
    def _errors(code):
        if code == 413:
            response = '图片体积太大。'
            return response
        elif code == 400:
            response = '你没上传图片？'
            return response
        elif code == 403:
            response = 'token无效。'
            return response
        elif code == 429:
            response = '请求太快了，缓一缓吧。'
            return response
        elif code == 500 or code == 503:
            response = '服务器错误 或者 你传错了图片格式。'
            return response
        else:
            response = '未知错误,请联系开发者'
            return response

    def me(self, key=None):  # 获取自己的信息
        try:
            params = None
            if key:
                params = {'key': key}
            res = requests.get(self.MeURL, params=params, verify=False, **self.requests_kwargs)
            if res.status_code == 200:
                data = res.json()
                return TraceMoeMe(data)
            else:
                logger.error(res.status_code)
        except Exception as e:
            logger.info(e)

    def search(self, url, key=None, anilistID=None, anilistInfo=True, cutBorders=True):
        """识别图片

        :param key: API密钥 https://soruly.github.io/trace.moe-api/#/limits?id=api-search-quota-and-limits
        :param url: 网络地址(http或https链接)或本地(本地图片路径)  When using video / gif, only the 1st frame would be extracted for searching.
        :param anilistID: 搜索限制为特定的 Anilist ID(默认无)
        :param anilistInfo: 详细信息(默认开启)
        :param cutBorders: 切割黑边框(默认开启)
        """
        try:
            headers = None
            params = dict()
            if anilistID:
                params['anilistID'] = anilistID
            if cutBorders:
                params['cutBorders'] = None
            if anilistInfo:
                params['anilistInfo'] = None
            if headers:
                headers = {"x-trace-key": key}
            if url[:4] == 'http':  # 网络url
                params['url'] = url
                res = requests.get(self.TraceMoeURL, headers=headers, params=params, verify=False,
                                   **self.requests_kwargs)
                if res.status_code == 200:
                    data = res.json()
                    return TraceMoeResponse(data, self.mute, self.size)
                else:
                    logger.error(self._errors(res.status_code))
            else:  # 是否是本地文件
                res = requests.post(self.TraceMoeURL, headers=headers,
                                    files={"image": open(url, "rb")}, **self.requests_kwargs)
                if res.status_code == 200:
                    data = res.json()
                    return TraceMoeResponse(data, self.mute, self.size)
                else:
                    logger.error(self._errors(res.status_code))
        except Exception as e:
            logger.info(e)
