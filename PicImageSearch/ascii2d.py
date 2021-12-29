import requests
import urllib3
from bs4 import BeautifulSoup
from loguru import logger
from requests_toolbelt import MultipartEncoder
from .Utils import Ascii2DResponse
import hashlib

class Ascii2D:
    """
    Ascii2D
    -----------
    Reverse image from https://ascii2d.net\n


    Params Keys
    -----------
    :param **requests_kwargs: proxy settings
    :param bovw: use ascii2d bovw search,boolean, default True
    """

    def __init__(self,bovw=True, **requests_kwargs):
        self.requests_kwargs = requests_kwargs
        self.bovw = bovw
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

    def search(self, url):
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
                m = MultipartEncoder(
                    fields={
                        'uri': url
                    }
                )
            else:  # 是否是本地文件
                ASCII2DURL = 'https://ascii2d.net/search/file'
                m = MultipartEncoder(
                    fields={
                        'file': ('filename', open(url, 'rb'), "type=multipart/form-data")
                    }
                )
            headers = {'Content-Type': m.content_type}
            urllib3.disable_warnings()
            res = requests.post(ASCII2DURL, headers=headers, data=m, verify=False, **self.requests_kwargs)

            if self.bovw and res.status_code == 200:
                #如果启用bovw选项，第一次请求是向服务器提交文件
                if url[:4] == 'http':
                    res = requests.get(url)
                    md5hash = hashlib.md5(res.content).hexdigest()
                    res = requests.get(f'https://ascii2d.net/search/bovw/{md5hash}',**self.requests_kwargs)
                else:
                    with open(url, 'rb') as f:
                        md5hash = hashlib.md5(f.read()).hexdigest()
                    res = requests.get(f'https://ascii2d.net/search/bovw/{md5hash}',**self.requests_kwargs)
            else:
                logger.error(res.status_code)
                logger.error(self._errors(res.status_code))

            if res.status_code == 200:
                return self._slice(res.text)
            else:
                logger.error(res.status_code)
                logger.error(self._errors(res.status_code))
        except Exception as e:
            logger.error(e)
