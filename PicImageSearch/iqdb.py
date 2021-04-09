import urllib3
import re

from loguru import logger
from requests_toolbelt import MultipartEncoder
from bs4 import BeautifulSoup
from typing import Union


class IqdbNorm:
    _URL = 'http://www.iqdb.org'

    def __init__(self, data):
        table = data.table
        self.content = ''
        self.url = ''
        self.title = ''
        self.thumbnail = ''
        self.size = ''
        self.similarity: float
        self._arrange(table)

    def _arrange(self, data):
        REGEXIQ = re.compile("[0-9]+")
        tbody = data.tr
        content = tbody.th.string
        self.content = content
        tbody = data.tr.next_sibling
        url = tbody.td.a['href'] if tbody.td.a['href'][:4] == "http" else "https:" + tbody.td.a['href']
        title = tbody.td.a.img['title']
        thumbnail = self._URL + tbody.td.a.img['src']
        tbody = tbody.next_sibling.next_sibling
        size = tbody.td.string
        tbody = tbody.next_sibling
        similarity_raw = REGEXIQ.search(tbody.td.string)
        similarity = float(similarity_raw.group(0))
        self.url = url
        self.title = title
        self.thumbnail = thumbnail
        self.size = size
        self.similarity = similarity

    def __repr__(self):
        return f'<NormIqdb(content={repr(self.content)}, similarity={repr(self.similarity)}'


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


class Iqdb:
    """
    Iqdb and Iqdb 3d
    -----------
    Reverse image from http://www.iqdb.org\n

    Return Attributes
    -----------
    • .origin = Raw data from scrapper\n
    • .raw = Simplified data from scrapper\n
    • .raw[0].content = First index of content <Index 0 `Best match` or Index 1 etc `Additional match`>\n
    • .raw[0].title = First index of title that was found\n
    • .raw[0].url = First index of url source that was found\n
    • .raw[0].thumbnail = First index of url image that was found\n
    • .raw[0].similarity = First index of similarity image that was found\n
    • .raw[0].size = First index detail of image size that was found
    """

    __slots__ = ('url', '**aiohttp request_kwargs')

    def __init__(self, session=None, *, lib='asyncio', loop=None, **requests_kwargs):
        self.url = 'http://www.iqdb.org/'
        self.url_3d = 'http://3d.iqdb.org/'
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

    async def search(self, url):
        try:
            if url[:4] == 'http':  # 网络url
                datas = {
                    "url": url
                }
                res = await self.session.post(self.url, data=datas, **self.requests_kwargs)
            else:  # 是否是本地文件
                m = MultipartEncoder(
                    fields={
                        'file': ('filename', open(url, 'rb'), "type=multipart/form-data")
                    }
                )
                headers = {'Content-Type': m.content_type}
                urllib3.disable_warnings()
                res = await self.session.post(self.url, headers=headers, **self.requests_kwargs)
            if res.status == 200:
                resp = await res.text()
                return IqdbResponse(resp)
            else:
                logger.error(self._errors(res.status))
        except Exception as e:
            logger.error(e)

    async def search_3d(self, url):
        try:
            if url[:4] == 'http':  # 网络url
                datas = {
                    "url": url
                }
                res = await self.session.post(self.url_3d, data=datas, **self.requests_kwargs)
            else:  # 是否是本地文件
                m = MultipartEncoder(
                    fields={
                        'file': ('filename', open(url, 'rb'), "type=multipart/form-data")
                    }
                )
                headers = {'Content-Type': m.content_type}
                urllib3.disable_warnings()
                res = await self.session.post(self.url_3d, headers=headers, **self.requests_kwargs)
            if res.status == 200:
                resp = await res.text()
                return IqdbResponse(resp)
            else:
                logger.error(self._errors(res.status))
        except Exception as e:
            logger.error(e)
