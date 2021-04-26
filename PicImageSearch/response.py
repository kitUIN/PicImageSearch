import json
import re

from bs4 import BeautifulSoup
from PicImageSearch.norm import Ascii2DNorm, BaiDuNorm, GoogleNorm, IqdbNorm, SauceNaoNorm, TraceMoeNorm

class Ascii2DResponse:
    def __init__(self, res):
        soup = BeautifulSoup(res, 'html.parser', from_encoding='utf-8')
        resp = soup.find_all(class_='row item-box')
        
        self.origin: list = resp
        self.raw: list = list()

        for a in range(1, len(self.origin)):
            detail = self.origin[a].contents
            self.raw.append(Ascii2DNorm(detail))

    def __repr__(self):
        return f'<Ascii2DResponse(count={repr(len(self.origin))}>'


class BaiDuResponse:
    def __init__(self, resp):
        self.url: str = resp.request.url  # 搜索结果地址
        self.similar = list()
        self.raw = list()
        self.origin: list = json.loads(re.search(pattern='cardData = (.+);window\.commonData', string=resp.text)[1])
        for i in self.origin:
            setattr(self, i['cardName'], i)
        if self.same:
            self.raw = [BaiDuNorm(x) for x in self.same['tplData']['list']]
            info = self.same['extData']['showInfo']
            for y in info:
                if y == 'other_info':
                    continue
                for z in info[y]:
                    try:
                        self.similar[info[y].index(z)][y] = z
                    except:
                        self.similar.append({y: z})
        self.item = [attr for attr in dir(self) if
                     not callable(getattr(self, attr)) and not attr.startswith(("__", 'origin', 'raw', 'same', 'url'))]


class GoogleResponse:
    def __init__(self, res):
        soup = BeautifulSoup(res, 'html.parser', from_encoding='utf-8')
        resp = soup.find_all(class_='g')
        self.origin: list = resp
        self.raw: list = list()

        for ele in self.origin:
            detail = ele.contents
            self.raw.append(GoogleNorm(detail))

    def __repr__(self):
        return f'<GoogleResponse(count{repr(len(self.origin))})>'


class IqdbResponse:
    def __init__(self, resp):
        self.origin: list = resp
        self.raw: list = list()
        self._slice(resp)

    def _slice(self, data):
        soup = BeautifulSoup(data, "html.parser", from_encoding='utf-8')
        pages = soup.find(attrs={"class": "pages"})
        for i in pages:
            if i == '\n' or str(i) == '<br/>' or 'Your image' in str(i):
                continue
            self.raw.append(IqdbNorm(i))

    def __repr__(self):
        return f'<IqdbResponse(count={repr(len(self.raw))})>'

    
class SauceNAOResponse:
    def __init__(self, resp):
        self.raw: list = []
        resp_header = resp['header']
        resp_results = resp['results']
        for i in resp_results:
            self.raw.append(SauceNaoNorm(i))
        self.origin: dict = resp
        self.short_remaining: int = resp_header['short_remaining']  # 每30秒访问额度
        self.long_remaining: int = resp_header['long_remaining']  # 每天访问额度
        self.user_id: int = resp_header['user_id']
        self.account_type: int = resp_header['account_type']
        self.short_limit: str = resp_header['short_limit']
        self.long_limit: str = resp_header['long_limit']
        self.status: int = resp_header['status']
        self.results_requested: int = resp_header['results_requested']
        self.search_depth: str = resp_header['search_depth']
        self.minimum_similarity: float = resp_header['minimum_similarity']
        self.results_returned: int = resp_header['results_returned']

    def __repr__(self):
        return (f'<SauceResponse(count={repr(len(self.raw))}, long_remaining={repr(self.long_remaining)}, '
                f'short_remaining={repr(self.short_remaining)})>')


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
