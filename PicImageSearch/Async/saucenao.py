from loguru import logger
from requests_toolbelt import MultipartEncoder

from .network import HandOver
from PicImageSearch.Utils import SauceNAOResponse


class AsyncSauceNAO(HandOver):
    SauceNAOURL = 'https://saucenao.com/search.php'

    def __init__(self, api_key: str = None, *, numres: int = 5, hide: int = 1, minsim: int = 30, output_type: int = 2,
                 testmode: int = 0, dbmask: int = None, dbmaski: int = None, db: int = 999, **requests_kwargs) -> None:
        """
        SauceNAO
        -----------
        Reverse image from https://saucenao.com\n


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
        super().__init__(**requests_kwargs)
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
        """
        SauceNAO
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
        :param url: network address or local

        further documentation visit https://saucenao.com/user.php?page=search-api
        """
        try:
            params = self.params
            headers = dict()
            m = None
            if url[:4] == 'http':  # 网络url
                params['url'] = url
                resp = await self.post(self.SauceNAOURL, _headers=headers, _data=m, _params=params)
            else:  # 文件
                resp = await self.post(self.SauceNAOURL, _headers=headers, _params=params,
                                       _files={'file': open(url, 'rb')})
            if resp.status_code == 200:
                data = resp.json()
                return SauceNAOResponse(data)
            else:
                logger.error(self._errors(resp.status_code))
        except Exception as e:
            logger.info(e)
