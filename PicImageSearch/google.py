import requests
from bs4 import BeautifulSoup
from loguru import logger
from requests_toolbelt import MultipartEncoder
from urllib.parse import quote
import re


class GoogleNorm:

    def __init__(self, data):
        self.thumbnail: list = list()
        self.titles: list = list()
        self.urls: list = list()
        self._arrange(data)

    def _arrange(self, data):
        get_data = self._getdata(data)
        self.titles = get_data['titles']
        self.urls = get_data['urls']
        self.thumbnail = get_data['thumbnail']

    @staticmethod
    def _getdata(datas):
        regex = re.compile(
            r"((http(s)?(\:\/\/))+(www\.)?([\w\-\.\/])*(\.[a-zA-Z]{2,3}\/?))[^\s\b\n|]*[^.,;:\?\!\@\^\$ -]")

        data = {
            'thumbnail': [],
            'titles': [],
            'urls': [],
        }

        for x in datas:
            try:
                origin = x.find_all('span')
                data['titles'].append(origin[0].string)
                url = x.find_all('a')
                data['urls'].append(url[0]['href'])
                dsc = regex.search(url[3]['href'])
                if re.findall('translate', dsc.group(1)):
                    dsc = regex.search(url[4]['href'])
                if re.findall('jpg|png', dsc.group(1)):
                    data['thumbnail'].append(dsc.group(1))
                else:
                    data['thumbnail'].append(None)
            except:
                pass

        return data

    def __repr__(self):
        return f'<NormGoogle(title={repr(self.titles)}, urls={self.urls}, thumbnail={self.thumbnail})>'


class GoogleResponse:

    def __init__(self, resp):
        self.origin: list = resp
        self.raw: list = list()

        for ele in self.origin:
            detail = ele.contents
            self.raw.append(GoogleNorm(detail))

    def __repr__(self):
        return f'<GoogleResponse(count{repr(len(self.origin))})>'


class Google:
    GOOGLEURL = 'http://www.google.com/searchbyimage'
    REGEX = re.compile(r'"(.*?)"')

    def __init__(self, **request_kwargs):
        params = dict()
        self.params = params
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
        }
        self.requests_kwargs = request_kwargs

    @staticmethod
    def _slice(res):
        soup = BeautifulSoup(res, 'html.parser', from_encoding='utf-8')
        resp = soup.find_all(class_='g')
        return GoogleResponse(resp)

    def search(self, url):
        params = self.params
        if url[:4] == 'http':
            urlimage_encd = quote(url, safe='')
            params['image_url'] = urlimage_encd
            response = requests.get(
                self.GOOGLEURL, allow_redirects=False, params=params, headers=self.header, **self.requests_kwargs)
            fetchUrl = self.REGEX.findall(response.text)
            url_clean = list(filter(bool, fetchUrl))
            data = url_clean[2]
        else:
            params['encoded_image'] = url
            multipart = {'encoded_image': (
                url, open(url, 'rb')), 'image_content': ''}
            response = requests.post(
                f"{self.GOOGLEURL}/upload", files=multipart, allow_redirects=False, headers=self.header, **self.requests_kwargs)
            data = response.headers['Location']
        if response.status_code == 302:
            resp = requests.get(data, headers=self.header)
            return self._slice(resp.text)
        else:
            logger.error(response.status_code)
