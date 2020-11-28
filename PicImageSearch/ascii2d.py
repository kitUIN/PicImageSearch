import requests
import urllib3
from bs4 import BeautifulSoup
from loguru import logger
from requests_toolbelt import MultipartEncoder


class Ascii2DNorm:
    URL = 'https://ascii2d.net'

    def __init__(self, data):
        self.thumbnail: list = list()
        self.detail: str = data[3].small.string
        self.titles: list = list()
        self.authors: list = list()
        self.authors_urls: list = list()
        self.urls: list = list()
        self.marks: list = list()
        self._arrange(data)

    def _arrange(self, data):
        o_url = data[3].find('div', class_="detail-box gray-link").contents
        urls = self._geturls(o_url)
        self.thumbnail.append(self.URL + data[1].find('img')['src'])
        self.urls = urls['urls']
        self.titles = urls['titles']
        self.authors = urls['authors']
        self.authors_urls = urls['authors_urls']
        self.marks = urls['mark']

    @staticmethod
    def _geturls(data):
        all_urls = {
            'urls': [],
            'titles': [],
            'authors_urls': [],
            'authors': [],
            'mark': []
        }

        for x in data:
            if x == '\n':
                continue
            origin = x.find_all('a')
            all_urls['urls'].append(origin[0]['href'])
            all_urls['titles'].append(origin[0].string)
            all_urls['authors_urls'].append(origin[1]['href'])
            all_urls['authors'].append(origin[1].string)
            all_urls['mark'].append(x.small.string)
        return all_urls

    def __repr__(self):
        return f'<NormAscii2D(title={repr(self.titles)}, authors={self.authors},mark={self.marks})>'


class Ascii2DResponse:

    def __init__(self, resp):
        self.origin: list = resp
        self.raw: list = list()

        for ele in self.origin:
            detail = ele.contents
            self.raw.append(Ascii2DNorm(detail))

    def __repr__(self):
        return f'<Ascii2DResponse(count={repr(len(self.origin))}>'


class Ascii2D:
    ASCII2DFILES = 'https://ascii2d.net/search/url/'
    ASCII2DURL = 'https://ascii2d.net/search/multi'

    def __init__(self, **requests_kwargs):
        self.requests_kwargs = requests_kwargs

    @staticmethod
    def _slice(res):
        soup = BeautifulSoup(res, 'html.parser', from_encoding='utf-8')
        resp = soup.find_all(class_='row item-box')
        return Ascii2DResponse(resp)

    @staticmethod
    def _errors(code):
        if code == '500':
            return '服务器错误'
        else:
            return '未知错误，请汇报给项目维护者'

    def search(self, url):
        if url[:4] == 'http':  # 网络url
            m = MultipartEncoder(
                fields={
                    'uri': url
                }
            )
            headers = {'Content-Type': m.content_type}
            urllib3.disable_warnings()
            res = requests.post(self.ASCII2DURL, headers=headers, data=m, verify=False, **self.requests_kwargs)
            if res.status_code == 200:
                return self._slice(res.text)
            else:
                logger.error(self._errors(res.status_code))
        else:  # 是否是本地文件
            m = MultipartEncoder(
                fields={
                    'file': ('filename', open(url, 'rb'), "type=multipart/form-data")
                }
            )
            headers = {'Content-Type': m.content_type}
            urllib3.disable_warnings()
            res = requests.post(self.ASCII2DFILES, headers=headers, data=m, verify=False, **self.requests_kwargs)
            if res.status_code == 200:
                return self._slice(res.text)
            else:
                logger.error(self._errors(res.status_code))
