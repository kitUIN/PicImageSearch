import urllib3

from bs4 import BeautifulSoup
from loguru import logger
from typing import Union
from requests_toolbelt import MultipartEncoder
from aiohttp.formdata import FormData


class Ascii2DNorm:
    URL = 'https://ascii2d.net'

    def __init__(self, data):
        self.thumbnail: str
        self.detail: str = data[3].small.string
        self.title: str
        self.authors: str
        self.authors_urls: str
        self.url: str
        self.marks: str
        self._arrange(data)

    def _arrange(self, data):
        o_url = data[3].find('div', class_="detail-box gray-link").contents
        urls = self._geturls(o_url)
        self.thumbnail = self.URL + data[1].find('img')['src']
        self.url = urls['url']
        self.title = urls['title']
        self.authors = urls['authors']
        self.authors_urls = urls['authors_urls']
        self.marks = urls['mark']

    @staticmethod
    def _geturls(data):
        all_urls = {
            'url': str,
            'title': str,
            'authors_urls': str,
            'authors': str,
            'mark': str
        }

        for x in data:
            if x == '\n':
                continue
            try:
                origin = x.find_all('a')
                all_urls['url'] = origin[0]['href']
                all_urls['title'] = origin[0].string
                all_urls['authors_urls'] = origin[1]['href']
                all_urls['authors'] = origin[1].string
                all_urls['mark'] = x.small.string
            except:
                pass
        return all_urls

    def __repr__(self):
        return f'<NormAscii2D(title={repr(self.title)}, authors={self.authors}, mark={self.marks})>'


class Ascii2DResponse:

    def __init__(self, resp):
        self.origin: list = resp
        self.raw: list = list()

        for a in range(1, len(self.origin)):
            detail = self.origin[a].contents
            self.raw.append(Ascii2DNorm(detail))

    def __repr__(self):
        return f'<Ascii2DResponse(count={repr(len(self.origin))}>'


class Ascii2D:

    def __init__(self, session=None, *, lib='asyncio', loop=None, **requests_kwargs):
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

    async def search(self, url):
        m = FormData()
        if url[:4] == 'http':  # 网络url
            ASCII2DURL = 'https://ascii2d.net/search/uri'
            m.add_field('uri', url)
        else:  # 是否是本地文件
            ASCII2DURL = 'https://ascii2d.net/search/file'
            m.add_field(
                'file', 
                open(url, 'rb'),
                content_type="multipart/form-data"
            )
        urllib3.disable_warnings()
        response = await self.session.post(ASCII2DURL, data=m, ssl=False, **self.requests_kwargs)
        if response.status == 200:
            resp = await response.text()
            return self._slice(resp)
        else:
            logger.error(response.status)
            logger.error(self._errors(response.status))
