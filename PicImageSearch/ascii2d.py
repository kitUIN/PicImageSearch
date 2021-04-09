import requests
import urllib3
from bs4 import BeautifulSoup
from loguru import logger
from requests_toolbelt import MultipartEncoder


class Ascii2DNorm:
    URL = 'https://ascii2d.net'

    def __init__(self, data):
        self.thumbnail = ""
        self.detail: str = data[3].small.string
        self.title = ""
        self.authors = ""
        self.url = ""
        self.marks = ""
        self._arrange(data)

    def _arrange(self, data):
        o_url = data[3].find('div', class_="detail-box gray-link").contents
        urls = self._geturls(o_url)
        self.thumbnail = self.URL + data[1].find('img')['src']
        self.url = urls['url']
        self.title = urls['title']
        self.authors = urls['authors']
        self.marks = urls['mark']

    @staticmethod
    def _geturls(data):
        all_urls = {
            'url': "",
            'title': "",
            'authors_urls': "",
            'authors': "",
            'mark': ""
        }

        for x in data:
            if x == '\n':
                continue
            try:
                origin = x.find_all('a')
                all_urls['url'] = origin[0]['href']
                all_urls['title'] = origin[0].string
                all_urls['authors_urls'] = origin[1]['href']
                all_urls['authors'] = origin[1].string
                all_urls['mark'] = x.small.string
            except:
                pass
        return all_urls

    def __repr__(self):
        return f'<NormAscii2D(title={repr(self.title)}, authors={self.authors}, mark={self.marks})>'


class Ascii2DResponse:

    def __init__(self, resp):
        self.origin: list = resp
        self.raw: list = list()

        for ele in self.origin:
            detail = ele.contents
            self.raw.append(Ascii2DNorm(detail))

    def __repr__(self):
        return f'<Ascii2DResponse(count={repr(len(self.origin))}>'


class Ascii2D:
    """
    Ascii2D
    -----------
    Reverse image from https://ascii2d.net\n


    Params Keys
    -----------
    :param **requests_kwargs: proxy settings
    """

    def __init__(self, **requests_kwargs):
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
            if res.status_code == 200:
                return self._slice(res.text)
            else:
                logger.error(res.status_code)
                logger.error(self._errors(res.status_code))
        except Exception as e:
            logger.error(e)
