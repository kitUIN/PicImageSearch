import requests
import urllib3
from loguru import logger
from requests_toolbelt import MultipartEncoder
from bs4 import BeautifulSoup


class IqdbNorm:
    _URL = 'http://www.iqdb.org'
    def __init__(self, data):
        table = data.table
        self.content = ''
        self.url = ''
        self.title = ''
        self.thumbnail = ''
        self.size = ''
        self.similarity = ''
        self._arrange(table)

    def _arrange(self, data):
        tbody = data.tr
        content = tbody.th.string
        self.content = content
        tbody = data.tr.next_sibling
        url = tbody.td.a['href']
        title = tbody.td.a.img['title']
        thumbnail = self._URL + tbody.td.a.img['src']
        tbody = tbody.next_sibling.next_sibling
        size = tbody.td.string
        tbody = tbody.next_sibling
        similarity = tbody.td.string
        self.url = url
        self.title = title
        self.thumbnail = thumbnail
        self.size = size
        self.similarity = similarity

    def __repr__(self):
        return f'<SauceResponse(content={repr(self.content)}, similarity={repr(self.similarity)}'


class IqdbResponse:
    def __init__(self, resp):
        self.origin: list = resp
        self.raw: list = list()
        self._slice(resp)

    def _slice(self, data):
        soup = BeautifulSoup(data, "html.parser", from_encoding='utf-8')
        pages = soup.find(attrs={"class": "pages"})
        for i in pages:
            if i == '\n' or str(i) == '<br/>' or 'Your image' in str(i):
                continue
            self.raw.append(IqdbNorm(i))

    def __repr__(self):
        return f'<IqdbResponse(count={repr(len(self.raw))})>'


class Iqdb:

    def __init__(self, **requests_kwargs):
        self.url = 'http://www.iqdb.org/'
        self.url_3d = 'http://3d.iqdb.org/'
        self.requests_kwargs = requests_kwargs

    def search(self, url):
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
                return IqdbResponse(res.content)
        except Exception as e:
            logger.error(e)

    def search_3d(self, url):
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
        except Exception as e:
            logger.error(e)
