from bs4 import BeautifulSoup
from loguru import logger

from .network import HandOver
from PicImageSearch.Utils import GoogleResponse
from urllib.parse import quote


class AsyncGoogle(HandOver):
    """
    Google
    -----------
    Reverse image from https://www.google.com\n


    Params Keys
    -----------
    :param **requests_kwargs: proxy settings
    """

    GOOGLEURL = 'https://www.google.com/searchbyimage'

    def __init__(self, **request_kwargs):
        super().__init__(**request_kwargs)
        params = dict()
        self.params = params
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
        }
        self.requests_kwargs = request_kwargs

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
        soup = BeautifulSoup(res, 'html.parser')
        resp = soup.find_all(class_='g')
        return GoogleResponse(resp)

    async def search(self, url):
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
        try:
            params = self.params
            if url[:4] == 'http':
                urlimage_encd = quote(url, safe='')
                params['image_url'] = urlimage_encd
                response = await self.get(
                    self.GOOGLEURL, _params=params, _headers=self.header)
            else:
                multipart = {'encoded_image': (
                    url, open(url, 'rb'))}
                response = await self.post(
                    f"{self.GOOGLEURL}/upload", _files=multipart, _headers=self.header)
            if response.status_code == 200:
                return self._slice(response.text)
            else:
                logger.error(self._errors(response.status_code))
        except Exception as e:
            logger.error(e)
