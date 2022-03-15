import httpx
from loguru import logger

from .Utils import get_error_message
from .Utils.iqdb import IqdbResponse


class Iqdb:
    """
    Iqdb and Iqdb 3d
    -----------
    Reverse image from https://iqdb.org\n


    Params Keys
    -----------
    :param **requests_kwargs: proxy settings
    """

    def __init__(self, **requests_kwargs):
        self.url = "https://iqdb.org/"
        self.url_3d = "https://3d.iqdb.org/"
        self.requests_kwargs = requests_kwargs

    def search(self, url) -> IqdbResponse:
        """
        Iqdb
        -----------
        Reverse image from https://iqdb.org\n


        Return Attributes
        -----------
        • .origin = Raw data from scrapper\n
        • .raw = Simplified data from scrapper\n
        • .saucenao = e.g.  https://saucenao.com/search.php?db=999&dbmaski=32768&url=https://iqdb.org/thu/thu_ccb14a40.jpg
        • .ascii2d = e.g.  https://ascii2d.net/search/url/https://iqdb.org/thu/thu_ccb14a40.jpg
        • .tineye = e.g.  https://tineye.com/search?url=https://iqdb.org/thu/thu_ccb14a40.jpg
        • .google = e.g.   https://www.google.com/searchbyimage?image_url=https://iqdb.org/thu/thu_ccb14a40.jpg&safe=off
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
            if url[:4] == "http":  # 网络url
                data = {"url": url}
                res = httpx.post(self.url, data=data, **self.requests_kwargs)
            else:  # 是否是本地文件
                files = {"file": open(url, "rb")}
                res = httpx.post(self.url, files=files, **self.requests_kwargs)
            if res.status_code == 200:
                # logger.info(res.text)
                return IqdbResponse(res.content)
            else:
                logger.error(get_error_message(res.status_code))
        except Exception as e:
            logger.error(e)

    def search_3d(self, url) -> IqdbResponse:
        """
        Iqdb 3D
        -----------
        Reverse image from https://3d.iqdb.org\n


        Return Attributes
        -----------
        • .origin = Raw data from scrapper\n
        • .raw = Simplified data from scrapper\n
        • .raw[0].content = First index of content <Index 0 `Best match` or Index 1 etc. `Additional match`>\n
        • .raw[0].title = First index of title that was found\n
        • .raw[0].url = First index of url source that was found\n
        • .raw[0].thumbnail = First index of url image that was found\n
        • .raw[0].similarity = First index of similarity image that was found\n
        • .raw[0].size = First index detail of image size that was found
        """
        try:
            if url[:4] == "http":  # 网络url
                data = {"url": url}
                res = httpx.post(self.url_3d, data=data, **self.requests_kwargs)
            else:  # 是否是本地文件
                files = {"file": open(url, "rb")}
                res = httpx.post(self.url_3d, files=files, **self.requests_kwargs)
            if res.status_code == 200:
                return IqdbResponse(res.content)
            else:
                logger.error(get_error_message(res.status_code))
        except Exception as e:
            logger.error(e)
