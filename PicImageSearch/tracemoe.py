import base64
from urllib import parse

import requests
from loguru import logger


class TraceMoeNorm:
    def __init__(self, data, mute=False):
        self.origin: dict = data
        self.From: int = data['from']  # 匹配场景的开始时间
        self.To: int = data['to']  # 匹配场景的结束时间
        self.anilist_id: int = data['anilist_id']  # 匹配的Anilist ID见https://anilist.co/
        self.at: int = data['at']  # 匹配场景的确切时间
        self.season: str = data['season']  # 发布时间
        self.anime: str = data['anime']  # 番剧名字
        self.filename: str = data['filename']  # 找到匹配项的文件名
        self.episode: int = data['episode']  # 估计的匹配的番剧的集数
        self.tokenthumb: str = data['tokenthumb']  # 用于生成预览的token
        self.similarity: float = float(data['similarity'])  # 相似度，相似性低于 87% 的搜索结果可能是不正确的结果
        self.title: str = data['title']  # 番剧名字
        self.title_native: str = data['title_native']  # 番剧世界命名
        self.title_chinese: str = data['title_chinese']  # 番剧中文命名
        self.title_english: str = data['title_english']  # 番剧英文命名
        self.title_romaji: str = data['title_romaji']  # 番剧罗马命名
        self.mal_id: int = data['mal_id']  # 匹配的MyAnimelist ID见https://myanimelist.net/
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
              "{}/{}?t={}&token={}".format(self.anilist_id, parse.quote(self.filename), self.at,
                                           self.tokenthumb)
        if mute:
            url = url + '&mute'
        return url

    def __repr__(self):
        return f'<NormTraceMoe(title={repr(self.title_chinese)}, similarity={self.similarity:.2f})>'


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

    def __init__(self, mute=False, **requests_kwargs):
        """
        :param mute: 预览视频是否静音（默认不静音）
        :param **requests_kwargs:代理设置
        """
        self.mute: bool = mute
        self.requests_kwargs = requests_kwargs

    @staticmethod
    def _base_64(filename):
        with open(filename, 'rb') as f:
            coding = base64.b64encode(f.read())  # 读取文件内容，转换为base64编码
            # print('本地base64转码~')
            return coding.decode()

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

    def search(self, url, Filter=0):
        """
        搜索
        :param url:网络地址或本地
        :param Filter: 搜索限制为特定的 Anilist ID(默认无)
        """
        try:
            params = dict()
            if url[:4] == 'http':  # 网络url
                params['url'] = url
                res = requests.get(self.TraceMoeURL, params=params, verify=False, **self.requests_kwargs)
                if res.status_code == 200:
                    data = res.json()
                    return TraceMoeResponse(data, self.mute)
                else:
                    logger.error(self._errors(res.status_code))
            else:  # 是否是本地文件
                img = self._base_64(url)
                res = requests.post(self.TraceMoeURL, json={"image": img, "filter": Filter}, **self.requests_kwargs)
                if res.status_code == 200:
                    data = res.json()
                    return TraceMoeResponse(data, self.mute)
                else:
                    logger.error(self._errors(res.status_code))
        except Exception as e:
            logger.info(e)

    @staticmethod
    def download_image(thumbnail, filename='image.png'):
        """
        下载缩略图
        :param filename: 重命名文件
        :param thumbnail:缩略图地址 见返回值中的thumbnail
        """
        with requests.get(thumbnail, stream=True) as resp:
            with open(filename, 'wb') as fd:
                for chunk in resp.iter_content():
                    fd.write(chunk)

    @staticmethod
    def download_video(video, filename='video.mp4'):
        """
        下载预览视频
        :param filename: 重命名文件
        :param video :缩略图地址 见返回值中的video_thumbnail
        """
        with requests.get(video, stream=True) as resp:
            with open(filename, 'wb') as fd:
                for chunk in resp.iter_content():
                    fd.write(chunk)
