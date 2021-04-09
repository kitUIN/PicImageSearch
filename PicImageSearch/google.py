import re

from aiohttp.formdata import FormData
from bs4 import BeautifulSoup
from loguru import logger
from urllib.parse import quote
from typing import Union


class GoogleNorm:
    def __init__(self, data):
        self.thumbnail = ""
        self.title = ""
        self.url = ""
        self._arrange(data)

    def _arrange(self, data):
        get_data = self._getdata(data)
        self.title = get_data['title']
        self.url = get_data['url']
        self.thumbnail = get_data['thumbnail']

    def _getdata(self, datas):

        data = {
            'thumbnail': "",
            'title': "",
            'url': "",
        }

        for x in datas:
            try:
                origin = x.find_all('h3')
                data['title'] = origin[0].string
                url = x.find_all('a')
                data['url'] = url[0]['href']
                img = self._gethumbnail(url)
                data['thumbnail'] = img
            except:
                pass

        return data

    @staticmethod
    def _gethumbnail(data):
        GOOGLEURL = "https://www.google.com/"
        regex = re.compile(
            r"((http(s)?(\:\/\/))+(www\.)?([\w\-\.\/])*(\.[a-zA-Z]{2,3}\/?))[^\s\b\n|]*[^.,;:\?\!\@\^\$ -]")

        thumbnail = "No directable url"

        for a in range(5):
            try:
                if re.findall('jpg|png', regex.search(data[a]['href']).group(1)):
                    thumbnail = regex.search(data[a]['href']).group(1)
                elif re.findall('/imgres', data[a]['href']):
                    thumbnail = f"{GOOGLEURL}{data[a]['href']}"
            except:
                continue

        return thumbnail

    def __repr__(self):
        return f'<NormGoogle(title={repr(self.title)}, url={self.url}, thumbnail={self.thumbnail})>'


class GoogleResponse:

    def __init__(self, resp):
        self.origin: list = resp
        self.raw: list = list()

        for ele in self.origin:
            detail = ele.contents
            self.raw.append(GoogleNorm(detail))

    def __repr__(self):
        return f'<GoogleResponse(count{repr(len(self.origin))})>'


class Google:
    """
    Google
    -----------
    Reverse image from https://www.google.com\n

    Return Attributes
    -----------
    • .origin = Raw data from scrapper\n
    • .raw = Simplified data from scrapper\n
    • .raw[2] = Second index of simplified data that was found <Should start from index 2, because from there is matching image>\n
    • .raw[2].title = First index of title that was found\n
    • .raw[2].url = First index of url source that was found\n
    • .raw[2].thumbnail = First index of url image that was found
    """

    __slots__ = ('url', '**aiohttp request_kwargs')
    GOOGLEURL = 'https://www.google.com/searchbyimage'

    def __init__(self, session=None, *, lib='asyncio', loop=None, **request_kwargs):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'
        }
        self.requests_kwargs = request_kwargs

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

    @staticmethod
    def _slice(res):
        soup = BeautifulSoup(res, 'html.parser', from_encoding='utf-8')
        resp = soup.find_all(class_='g')
        return GoogleResponse(resp)

    async def search(self, url):
        try:
            if url[:4] == 'http':
                params = {
                    'image_url': quote(url, safe='')
                }
                response = await self.session.get(
                    self.GOOGLEURL, params=params, headers=self.header, **self.requests_kwargs)
            else:
                m = FormData()
                m.add_field(
                    'encoded_image',
                    open(url, 'rb'), 
                    content_type="multipart/form-data"
                )
                response = await self.session.post(
                    f"{self.GOOGLEURL}/upload", data=m, headers=self.header, **self.requests_kwargs)
            if response.status == 200:
                resp = await response.text()
                return self._slice(resp)
            else:
                logger.error(self._errors(response.status))
        except Exception as e:
            logger.error(e)
