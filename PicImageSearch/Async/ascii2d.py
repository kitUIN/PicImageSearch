import requests
import urllib3
from bs4 import BeautifulSoup
from loguru import logger
from requests_toolbelt import MultipartEncoder

from .network import HandOver
from PicImageSearch.Utils import Ascii2DResponse




class AsyncAscii2D(HandOver):
    """
    Ascii2D
    -----------
    Reverse image from https://ascii2d.net\n


    Params Keys
    -----------
    :param **requests_kwargs: proxy settings
    """

    def __init__(self, **requests_kwargs):
        super().__init__(**requests_kwargs)
        self.requests_kwargs = requests_kwargs

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
            if url[:4] == 'http':  # 网络url
                ASCII2DURL = 'https://ascii2d.net/search/uri'
                res = await self.post(ASCII2DURL, _data={"uri": url})
            else:  # 是否是本地文件
                ASCII2DURL = 'https://ascii2d.net/search/file'
                res = await self.post(ASCII2DURL, _files={"file": open(url, 'rb')})

            if res.status_code == 200:
                return self._slice(res.text)
            else:
                logger.error(res.status_code)
                logger.error(self._errors(res.status_code))
        except Exception as e:
            logger.error(e)
