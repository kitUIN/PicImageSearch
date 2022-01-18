import requests
import urllib3
from loguru import logger
from requests_toolbelt import MultipartEncoder

from PicImageSearch.Utils.iqdb import IqdbResponse


class Iqdb:
    """
    Iqdb and Iqdb 3d
    -----------
    Reverse image from http://www.iqdb.org\n


    Params Keys
    -----------
    :param **requests_kwargs: proxy settings
    """

    def __init__(self, **requests_kwargs):
        self.url = 'http://www.iqdb.org/'
        self.url_3d = 'http://3d.iqdb.org/'
        self.requests_kwargs = requests_kwargs

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

    def search(self, url)-> IqdbResponse:
        """
        Iqdb
        -----------
        Reverse image from http://www.iqdb.org\n


        Return Attributes
        -----------
        • .origin = Raw data from scrapper\n
        • .raw = Simplified data from scrapper\n
        • .saucenao = eg.  https://saucenao.com/search.php?db=999&dbmaski=32768&url=https://iqdb.org/thu/thu_ccb14a40.jpg
        • .ascii2d = eg.  https://ascii2d.net/search/url/https://iqdb.org/thu/thu_ccb14a40.jpg
        • .tineye = eg.  https://tineye.com/search?url=https://iqdb.org/thu/thu_ccb14a40.jpg
        • .google = eg.   https://www.google.com/searchbyimage?image_url=https://iqdb.org/thu/thu_ccb14a40.jpg&safe=off
        • .more = other (low similarity) Simplified data from scrapper\n
        • .raw[0].content = First index of content <Index 0 `Best match` or Index 1 etc `Additional match`>\n
        • .raw[0].source = First index of source website that was found\n
        • .raw[0].other_source = other index of source website that was found\n
        • .raw[0].url = First index of url source that was found\n
        • .raw[0].thumbnail = First index of url image that was found\n
        • .raw[0].similarity = First index of similarity image that was found\n
        • .raw[0].size = First index detail of image size that was found

        """
        try:
            if url[:4] == 'http':  # 网络url
                datas = {
                    "url": url
                }
                res = requests.post(self.url, data=datas, **self.requests_kwargs)
            else:  # 是否是本地文件
                m = MultipartEncoder(
                    fields={
                        'file': ('filename', open(url, 'rb'), "type=multipart/form-data")
                    }
                )
                headers = {'Content-Type': m.content_type}
                urllib3.disable_warnings()
                res = requests.post(self.url, headers=headers, **self.requests_kwargs)
            if res.status_code == 200:
                # logger.info(res.text)
                return IqdbResponse(res.content)
            else:
                logger.error(self._errors(res.status_code))
        except Exception as e:
            logger.error(e)

    def search_3d(self, url) -> IqdbResponse:
        """
        Iqdb 3D
        -----------
        Reverse image from http://3d.iqdb.org\n
        

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
        try:
            if url[:4] == 'http':  # 网络url
                datas = {
                    "url": url
                }
                res = requests.post(self.url_3d, data=datas, **self.requests_kwargs)
            else:  # 是否是本地文件
                m = MultipartEncoder(
                    fields={
                        'file': ('filename', open(url, 'rb'), "type=multipart/form-data")
                    }
                )
                headers = {'Content-Type': m.content_type}
                urllib3.disable_warnings()
                res = requests.post(self.url_3d, headers=headers, **self.requests_kwargs)
            if res.status_code == 200:
                return IqdbResponse(res.content)
            else:
                logger.error(self._errors(res.status_code))
        except Exception as e:
            logger.error(e)
