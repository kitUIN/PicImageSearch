import urllib3

from bs4 import BeautifulSoup
from loguru import logger
from typing import Union
from requests_toolbelt import MultipartEncoder
from aiohttp.formdata import FormData


class Ascii2DNorm:
    URL = 'https://ascii2d.net'

    def __init__(self, data):
        self.thumbnail = ""
        self.detail: str = data[3].small.string
        self.title = ""
        self.authors = ""
        self.url = ""
        self.marks = ""
        self._arrange(data)

    def _arrange(self, data):
        o_url = data[3].find('div', class_="detail-box gray-link").contents
        urls = self._geturls(o_url)
        self.thumbnail = self.URL + data[1].find('img')['src']
        self.url = urls['url']
        self.title = urls['title']
        self.authors = urls['authors']
        self.marks = urls['mark']

    @staticmethod
    def _geturls(data):
        all_urls = {
            'url': "",
            'title': "",
            'authors_urls': "",
            'authors': "",
            'mark': ""
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
    """
    Ascii2D
    -----------
    Reverse image from https://ascii2d.net\n

    Return Attributes
    -----------
    • .origin = Raw data from scrapper\n
    • .raw = Simplified data from scrapper\n
    • .raw[0] = First index of simplified data that was found\n
    • .raw[0].title = First index of title that was found\n
    • .raw[0].url = First index of url source that was found\n
    • .raw[0].authors = First index of authors that was found\n
    • .raw[0].thumbnail = First index of url image that was found\n
    • .raw[0].detail = First index of details image that was found
    """

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
                logger.error(self._errors(response.status))
        except Exception as e:
            logger.error(e)
