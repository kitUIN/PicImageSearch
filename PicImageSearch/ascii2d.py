import cloudscraper
from bs4 import BeautifulSoup
from loguru import logger
from requests_toolbelt import MultipartEncoder
from .Utils import Ascii2DResponse, get_error_message


class Ascii2D:
    """
    Ascii2D
    -----------
    Reverse image from https://ascii2d.net\n


    Params Keys
    -----------
    :param **requests_kwargs:   proxy settings.\n
    :param bovw(boolean):   use ascii2d bovw search, default False \n
    """

    def __init__(self, bovw=False, **requests_kwargs):
        self.requests_kwargs = requests_kwargs
        self.bovw = bovw

    @staticmethod
    def _slice(res) -> Ascii2DResponse:
        soup = BeautifulSoup(res, 'html.parser')
        resp = soup.find_all(class_='row item-box')
        return Ascii2DResponse(resp)

    def search(self, url) -> Ascii2DResponse:
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
        scraper = cloudscraper.create_scraper({'browser': 'chrome',
                                               'platform': 'windows',
                                               'mobile': False
                                               })
        try:
            if url[:4] == 'http':  # 网络url
                ascii2d_url = 'https://ascii2d.net/search/uri'
                m = MultipartEncoder(
                    fields={
                        'uri': url
                    }
                )
            else:  # 是否是本地文件
                ascii2d_url = 'https://ascii2d.net/search/file'
                m = MultipartEncoder(
                    fields={
                        'file': ('filename', open(url, 'rb'), "type=multipart/form-data")
                    }
                )
            headers = {'Content-Type': m.content_type}
            res = scraper.post(ascii2d_url, headers=headers, data=m, **self.requests_kwargs)
            if res.status_code == 200:
                if self.bovw:
                    # 如果启用bovw选项，第一次请求是向服务器提交文件
                    res = scraper.get(res.url.replace('/color/', '/bovw/'), **self.requests_kwargs)
            else:
                logger.error(res.status_code)
                logger.error(get_error_message(res.status_code))

            if res.status_code == 200:
                return self._slice(res.text)
            else:
                logger.error(res.status_code)
                logger.error(get_error_message(res.status_code))
        except Exception as e:
            logger.error(e)
