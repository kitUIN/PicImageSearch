import requests
import urllib3

from loguru import logger
from typing import Union
from aiohttp.formdata import FormData

class SauceNaoNorm:
    def __init__(self, data):
        result_header = data['header']
        result_data = data['data']
        self.raw: dict = data
        self.similarity: float = float(result_header['similarity'])
        self.thumbnail: str = result_header['thumbnail']
        self.index_id: int = result_header['index_id']
        self.index_name: str = result_header['index_name']
        self.title: str = self._get_title(result_data)
        self.url: str = self._get_url(result_data)
        self.author: str = self._get_author(result_data)
        self.pixiv_id: str = self._get_pixiv_id(result_data)
        self.member_id: str = self._get_member_id(result_data)

    def download_thumbnail(self, filename='thumbnail.png'):  # 缩略图生成
        with requests.get(self.thumbnail, stream=True) as resp:
            with open(filename, 'wb') as fd:
                for chunk in resp.iter_content():
                    fd.write(chunk)

    @staticmethod
    def _get_title(data):
        if 'title' in data:
            return data['title']
        elif 'eng_name' in data:
            return data['eng_name']
        elif 'material' in data:
            return data['material']
        elif 'source' in data:
            return data['source']
        elif 'created_at' in data:
            return data['created_at']

    @staticmethod
    def _get_url(data):
        if 'ext_urls' in data:
            return data['ext_urls'][0]
        elif 'getchu_id' in data:
            return f'http://www.getchu.com/soft.phtml?id={data["getchu_id"]}'
        return ''

    @staticmethod
    def _get_author(data):
        if 'author' in data:
            return data['author']
        elif 'author_name' in data:
            return data['author_name']
        elif 'member_name' in data:
            return data['member_name']
        elif 'pawoo_user_username' in data:
            return data['pawoo_user_username']
        elif 'company' in data:
            return data['company']
        elif 'creator' in data:
            if isinstance(data['creator'], list):
                return data['creator'][0]
            return data['creator']

    @staticmethod
    def _get_pixiv_id(data):
        if 'pixiv_id' in data:
            return data['pixiv_id']
        else:
            return ''

    @staticmethod
    def _get_member_id(data):
        if 'member_id' in data:
            return data['member_id']
        else:
            return ''

    def __repr__(self):
        return f'<NormSauceNao(title={repr(self.title)}, similarity={self.similarity:.2f})>'


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


class SauceNAO:
    SauceNAOURL = 'https://saucenao.com/search.php'

    def __init__(self, 
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

        # minsim 控制最小相似度
        self.requests_kwargs = requests_kwargs
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
        self.params = params

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

    async def search(self, url: str):
        try:
            params = self.params
            # headers = {}
            m = FormData()
            if url[:4] == 'http':  # 网络url
                params['url'] = url
            else:  # 文件
                m.add_field(
                    'file',
                    open(url, 'rb'),
                    content_type="multipart/form-data"
                )
            urllib3.disable_warnings()
            resp = await self.session.post(self.SauceNAOURL, data=m, params=params, ssl=False,
                                **self.requests_kwargs)
            if resp.status == 200:
                data = await resp.json()
                return SauceNAOResponse(data)
            else:
                logger.error(self._errors(resp.status))
        except Exception as a:
            logger.info(a)
        
