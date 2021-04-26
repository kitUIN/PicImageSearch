import base64

from typing import Union
from loguru import logger
from requests_toolbelt import MultipartEncoder
from urllib.parse import quote
from PicImageSearch.response import Ascii2DResponse, GoogleResponse, IqdbResponse, SauceNAOResponse, TraceMoeResponse


class Search:
    def __init__(self, session=None, *, lib='asyncio', loop=None):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'
        }
        if lib not in ('asyncio', 'multio'):
            raise ValueError(
                f"lib must be of type `str` and be either `asyncio' not '{lib if isinstance(lib, str) else lib.__class__.__name__}'")
        self._lib = lib
        if lib == 'asyncio':
            import asyncio
            loop = loop or asyncio.get_event_loop()
        self.session = session or self._make_session(lib, loop)

    @staticmethod
    def _make_session(lib, loop=None) -> Union['aiohttp.ClientSession']:
        try:
            import aiohttp
        except ImportError:
            raise ImportError(
                "To use PicImageSearch in asyncio mode, it requires `aiohttp` module.")
        return aiohttp.ClientSession(loop=loop)

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

    async def ascii2d(self, url, **requests_kwargs):
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
        try:
            from aiohttp.formdata import FormData
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
            # urllib3.disable_warnings()
            response = await self.session.post(ASCII2DURL, data=m, ssl=False, **requests_kwargs)
            if response.status == 200:
                resp = await response.text()
                return Ascii2DResponse(resp)
            else:
                logger.error(self._errors(response.status))
        except Exception as e:
            logger.error(e)

    async def baidu(self, url, **requests_kwargs):
        """
        Still on work
        """
        pass

    async def google(self, url, **requests_kwargs):
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
        GOOGLEURL = 'https://www.google.com/searchbyimage'

        try:
            if url[:4] == 'http':
                params = {
                    'image_url': quote(url, safe='')
                }
                response = await self.session.get(
                    GOOGLEURL, params=params, headers=self.header, **requests_kwargs)
            else:
                from aiohttp.formdata import FormData
                m = FormData()
                m.add_field(
                    'encoded_image',
                    open(url, 'rb'),
                    content_type="multipart/form-data"
                )
                response = await self.session.post(
                    f"{GOOGLEURL}/upload", data=m, headers=self.header, **requests_kwargs)
            if response.status == 200:
                resp = await response.text()
                return GoogleResponse(resp)
            else:
                logger.error(self._errors(response.status))
        except Exception as e:
            logger.error(e)

    async def iqdb(self, url, **requests_kwargs):
        """
        Iqdb
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
        IQDB = 'http://www.iqdb.org/'
        try:
            if url[:4] == 'http':  # 网络url
                datas = {
                    "url": url
                }
                res = await self.session.post(IQDB, data=datas, **requests_kwargs)
            else:  # 是否是本地文件
                m = MultipartEncoder(
                    fields={
                        'file': ('filename', open(url, 'rb'), "type=multipart/form-data")
                    }
                )
                headers = {'Content-Type': m.content_type}
                # urllib3.disable_warnings()
                res = await self.session.post(IQDB, headers=headers, **requests_kwargs)
            if res.status == 200:
                resp = await res.text()
                return IqdbResponse(resp)
            else:
                logger.error(self._errors(res.status))
        except Exception as e:
            logger.error(e)

    async def iqdb_3d(self, url, **requests_kwargs):
        """
        Iqdb 3D
        -----------
        Reverse image from http://3d.iqdb.org/\n

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
        IQDB3D = 'http://3d.iqdb.org/'
        try:
            if url[:4] == 'http':  # 网络url
                datas = {
                    "url": url
                }
                res = await self.session.post(IQDB3D, data=datas, **requests_kwargs)
            else:  # 是否是本地文件
                m = MultipartEncoder(
                    fields={
                        'file': ('filename', open(url, 'rb'), "type=multipart/form-data")
                    }
                )
                headers = {'Content-Type': m.content_type}
                # urllib3.disable_warnings()
                res = await self.session.post(IQDB3D, headers=headers, **requests_kwargs)
            if res.status == 200:
                resp = await res.text()
                return IqdbResponse(resp)
            else:
                logger.error(self._errors(res.status))
        except Exception as e:
            logger.error(e)

    async def saucenao(self,
                       url: str,
                       api_key: str = None,
                       *, numres: int = 5,
                       hide: int = 1,
                       minsim: int = 30,
                       output_type: int = 2,
                       testmode: int = 0,
                       dbmask: int = None,
                       dbmaski: int = None,
                       db: int = 999,
                       session=None,
                       lib='asyncio',
                       loop=None,
                       **requests_kwargs
                       ) -> None:
        """
        SauceNao
        -----------
        Reverse image from https://saucenao.com\n
        Return Attributes
        -----------
        • .origin = Raw data from scrapper\n
        • .raw = Simplified data from scrapper\n
        • .raw[0] = First index of simplified data that was found\n
        • .raw[0].title = First index of title that was found\n
        • .raw[0].url = First index of url source that was found\n
        • .raw[0].thumbnail = First index of url image that was found\n
        • .raw[0].similarity = First index of similarity image that was found\n
        • .raw[0].author = First index of author image that was found\n
        • .raw[0].pixiv_id = First index of pixiv id that was found\n
        • .raw[0].member_id = First index of memeber id that was found\n
        • .long_remaining = Available limmits API in a day <day limit>\n
        • .short_remaining = Available limmits API in a day <day limit>\n
        Params Keys
        -----------
        :param api_key: (str) Access key for SauceNAO (default=None)
        :param output_type:(int) 0=normal (default) html 1=xml api (not implemented) 2=json api default=2
        :param testmode:(int) Test mode 0=normal 1=test (default=0)
        :param numres:(int) output number (default=5)
        :param dbmask:(int) The mask used to select the specific index to be enabled (default=None)
        :param dbmaski:(int) is used to select the mask of the specific index to be disabled (default=None)
        :param db:(int)Search for a specific index number or all indexes (default=999), see https://saucenao.com/tools/examples/api/index_details.txt
        :param minsim:(int)Control the minimum similarity (default=30)
        :param hide:(int) result hiding control, none=0, clear return value (default)=1, suspect return value=2, all return value=3
        """

        SAUCENAO = 'https://saucenao.com/search.php'

        params = {
            'testmode': testmode,
            'numres': numres,
            'output_type': output_type,
            'hide': hide,
            'db': db,
            'minsim': minsim
        }
        if api_key is not None:
            params['api_key'] = api_key
        if dbmask is not None:
            params['dbmask'] = dbmask
        if dbmaski is not None:
            params['dbmaski'] = dbmaski

        try:
            # headers = {}
            from aiohttp.formdata import FormData
            m = FormData()
            if url[:4] == 'http':  # 网络url
                params['url'] = url
            else:  # 文件
                m.add_field(
                    'file',
                    open(url, 'rb'),
                    content_type="multipart/form-data"
                )
            # urllib3.disable_warnings()
            resp = await self.session.post(SAUCENAO, data=m, params=params, ssl=False, **requests_kwargs)
            if resp.status == 200:
                data = await resp.json()
                return SauceNAOResponse(data)
            else:
                logger.error(self._errors(resp.status))
        except Exception as a:
            logger.info(a)

    async def tracemoe(self, url, Filter=0, **requests_kwargs):
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
        TRACEMOE = 'https://trace.moe/api/search'
        try:
            params = dict()
            if url[:4] == 'http':  # 网络url
                params['url'] = url
                res = await self.session.get(TRACEMOE, params=params, ssl=False, **requests_kwargs)
                if res.status == 200:
                    data = await res.json()
                    return TraceMoeResponse(data, self.mute)
                else:
                    logger.error(self._errors(res.status_code))
            else:  # 是否是本地文件
                img = self._base_64(url)
                res = await self.session.post(TRACEMOE, json={"image": img, "filter": Filter}, **requests_kwargs)
                if res.status == 200:
                    data = await res.json()
                    return TraceMoeResponse(data, self.mute)
                else:
                    logger.error(self._errors(res.status_code))
        except Exception as e:
            logger.info(e)
