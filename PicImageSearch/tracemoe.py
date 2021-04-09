import base64
from urllib import parse
from typing import Union

import requests
from loguru import logger


class TraceMoeNorm:
    def __init__(self, data, mute=False):
        self.origin: dict = data
        self.From: int = data['from']  # 匹配场景的开始时间
        self.To: int = data['to']  # 匹配场景的结束时间
        # 匹配的Anilist ID见https://anilist.co/
        self.anilist_id: int = data['anilist_id']
        self.at: int = data['at']  # 匹配场景的确切时间
        self.season: str = data['season']  # 发布时间
        self.anime: str = data['anime']  # 番剧名字
        self.filename: str = data['filename']  # 找到匹配项的文件名
        self.episode: int = data['episode']  # 估计的匹配的番剧的集数
        self.tokenthumb: str = data['tokenthumb']  # 用于生成预览的token
        self.similarity: float = float("{:.2f}".format(
            data['similarity'] * 100))  # 相似度，相似性低于 87% 的搜索结果可能是不正确的结果
        self.title: str = data['title']  # 番剧名字
        self.title_native: str = data['title_native']  # 番剧世界命名
        self.title_chinese: str = data['title_chinese']  # 番剧中文命名
        self.title_english: str = data['title_english']  # 番剧英文命名
        self.title_romaji: str = data['title_romaji']  # 番剧罗马命名
        # 匹配的MyAnimelist ID见https://myanimelist.net/
        self.mal_id: int = data['mal_id']
        self.synonyms: list = data['synonyms']  # 备用英文标题
        self.synonyms_chinese: list = data['synonyms_chinese']  # 备用中文标题
        self.is_adult: bool = data['is_adult']  # 是否R18
        self.thumbnail: str = self._preview_image()
        self.video_thumbnail: str = self._preview_video(mute)

    def _preview_image(self):  # 图片预览图
        # parse.quote()用于网页转码
        url = "https://trace.moe/thumbnail.php" \
              "?anilist_id={}&file={}&t={}&token={}".format(self.anilist_id, parse.quote(self.filename), self.at,
                                                            self.tokenthumb)
        return url

    def _preview_video(self, mute=False):
        """
        创建预览视频
        :param mute:预览视频是否静音，True为静音
        :return: 预览视频url地址
        """
        url = "https://media.trace.moe/video/" \
              f"{self.anilist_id}/{parse.quote(self.filename)}?t={self.at}&token={self.tokenthumb}"
        if mute:
            url = url + '&mute'
        return url

    @staticmethod
    def download_image(self, filename='image.png'):
        """
        下载缩略图
        :param filename: 重命名文件
        """
        with requests.get(self.thumbnail, stream=True) as resp:
            with open(filename, 'wb') as fd:
                for chunk in resp.iter_content():
                    fd.write(chunk)

    def download_video(self, filename='video.mp4'):
        """
        下载预览视频
        :param filename: 重命名文件
        """
        with requests.get(self.video_thumbnail, stream=True) as resp:
            with open(filename, 'wb') as fd:
                for chunk in resp.iter_content():
                    fd.write(chunk)

    def __repr__(self):
        return f'<NormTraceMoe(title={repr(self.title_native)}, similarity={self.similarity})>'


class TraceMoeResponse:
    def __init__(self, resp, mute):
        self.raw: list = []
        resp_docs = resp['docs']
        for i in resp_docs:
            self.raw.append(TraceMoeNorm(i, mute=mute))
        self.origin: dict = resp
        self.RawDocsCount: int = resp['RawDocsCount']  # 搜索的帧总数
        self.RawDocsSearchTime: int = resp['RawDocsSearchTime']  # 从数据库检索帧所用的时间
        self.ReRankSearchTime: int = resp['ReRankSearchTime']  # 比较帧所用的时间
        self.CacheHit: bool = resp['CacheHit']  # 是否缓存搜索结果
        self.trial: int = resp['trial']  # 搜索时间
        self.limit: int = resp['limit']  # 剩余搜索限制数
        self.limit_ttl: int = resp['limit_ttl']  # 限制重置之前的时间（秒）
        self.quota: int = resp['quota']  # 剩余搜索配额数
        self.quota_ttl: int = resp['quota_ttl']  # 配额重置之前的时间（秒）

    def __repr__(self):
        return (f'<TraceMoeResponse(count={repr(len(self.raw))}, RawDocsCount={repr(self.RawDocsCount)}, '
                f'RawDocsSearchTime={repr(self.RawDocsSearchTime)},trial={repr(self.trial)})>')


class TraceMoe:
    TraceMoeURL = 'https://trace.moe/api/search'

    def __init__(self, session=None, *, lib='asyncio', loop=None, mute=False, **requests_kwargs):
        """
        :param mute: 预览视频是否静音（默认不静音）
        :param **requests_kwargs:代理设置
        """
        self.mute: bool = mute
        self.requests_kwargs = requests_kwargs

        if lib not in ('asyncio', 'multio'):
            raise ValueError(
                f"lib must be of type `str` and be either `asyncio` or `multio`, not '{lib if isinstance(lib, str) else lib.__class__.__name__}'")
        self._lib = lib
        if lib == 'asyncio':
            import asyncio
            loop = loop or asyncio.get_event_loop()
        self.session = session or self._make_session(lib, loop)

    @staticmethod
    def _make_session(lib, loop=None) -> Union['aiohttp.ClientSession', 'asks.Session']:
        if lib == 'asyncio':
            try:
                import aiohttp
            except ImportError:
                raise ImportError(
                    "To use PicImageSearch in asyncio mode, it requires `aiohttp` module.")
            return aiohttp.ClientSession(loop=loop)
        try:
            import asks
        except ImportError:
            raise ImportError(
                "To use PicImageSearch in curio/trio mode, it requires `asks` module.")
        return asks.Session()

    @staticmethod
    def _base_64(filename):
        with open(filename, 'rb') as f:
            coding = base64.b64encode(f.read())  # 读取文件内容，转换为base64编码
            # print('本地base64转码~')
            return coding.decode()

    @staticmethod
    def _errors(code):
        if code == 404:
            return "Source down"
        elif code == 302:
            return "Moved temporarily, or blocked by captcha"
        elif code == 413 or code == 430:
            return "image too large"
        elif code == 400:
            return "Did you have upload the image ?, or wrong request syntax"
        elif code == 403:
            return "Forbidden,or token unvalid"
        elif code == 429:
            return "Too many request"
        elif code == 500 or code == 503:
            return "Server error, or wrong picture format"
        else:
            return "Unknown error, please report to the project maintainer"

    async def search(self, url, Filter=0):
        """
        TraceMoe
        -----------
        Reverse image from https://trace.moe\n
        Return Attributes
        -----------
        • .origin = Raw data from scrapper\n
        • .raw = Simplified data from scrapper\n
        • .raw[0] = First index of simplified data that was found\n
        • .raw[0].title = First index of title that was found\n
        • .raw[0].title_english = First index of english title that was found\n
        • .raw[0].title_chinese = First index of chinese title that was found\n
        • .raw[0].video_thumbnail = First index of url video that was found\n
        • .raw[0].thumbnail = First index of url image that was found\n
        • .raw[0].similarity = First index of similarity video that was found\n
        • .raw[0].From = First index of Starting time of the matching scene that was found\n
        • .raw[0].To = First index of Ending time of the matching scene that was found\n
        • .raw[0].at = First index of Exact time of the matching scene that was found\n
        • .raw[0].anilist_id = First index of The matching AniList ID that was found\n
        • .raw[0].season = First index of Season that was found\n
        • .raw[0].anime = First index of Anime name that was found\n
        • .raw.RawDocsCount = Total number of frames searched\n
        • .raw.RawDocsSearchTime = Time taken to retrieve the frames from database (sum of all cores)\n
        • .raw.ReRankSearchTime = Time taken to compare the frames (sum of all cores)\n
        • .trial = Time taken to compare the frames (sum of all cores)
        Params Keys
        -----------
        :param url: network address or local
        :param Filter: The search is restricted to a specific Anilist ID (default none)
        further documentation visit https://soruly.github.io/trace.moe/#/
        """
        try:
            params = dict()
            if url[:4] == 'http':  # 网络url
                params['url'] = url
                res = await self.session.get(self.TraceMoeURL, params=params, ssl=False, **self.requests_kwargs)
                if res.status == 200:
                    data = await res.json()
                    return TraceMoeResponse(data, self.mute)
                else:
                    logger.error(self._errors(res.status_code))
            else:  # 是否是本地文件
                img = self._base_64(url)
                res = await self.session.post(self.TraceMoeURL, json={"image": img, "filter": Filter}, **self.requests_kwargs)
                if res.status == 200:
                    data = await res.json()
                    return TraceMoeResponse(data, self.mute)
                else:
                    logger.error(self._errors(res.status_code))
        except Exception as e:
            logger.info(e)
