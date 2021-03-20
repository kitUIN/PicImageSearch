import json
import re

import requests
import urllib3
from requests import Response
from requests_toolbelt import MultipartEncoder


class BaiDuNorm:
    def __init__(self, data):
        self.origin: dict = data
        self.page_title: str = data['fromPageTitle']
        self.title: str = data['title'][0]
        self.abstract: str = data['abstract']
        self.image_src: str = data['image_src']
        self.url: str = data['url']
        self.img = list()
        if 'imgList' in data:
            self.img: list = data['imgList']

    def __repr__(self):
        return f'<NormSauce(title={repr(self.title)})>'


class BaiDuResponse:
    def __init__(self, resp: Response):
        self.url: str = resp.request.url  # 搜索结果地址
        self.similar = list()
        self.raw = list()
        self.origin: list = json.loads(re.search(pattern='cardData = (.+);window\.commonData', string=resp.text)[1])
        for i in self.origin:
            setattr(self, i['cardName'], i)
        if self.same:
            self.raw = [BaiDuNorm(x) for x in self.same['tplData']['list']]
            info = self.same['extData']['showInfo']
            for y in info:
                if y == 'other_info':
                    continue
                for z in info[y]:
                    try:
                        self.similar[info[y].index(z)][y] = z
                    except:
                        self.similar.append({y: z})
        self.item = [attr for attr in dir(self) if
                     not callable(getattr(self, attr)) and not attr.startswith(("__", 'origin', 'raw', 'same', 'url'))]

    def __repr__(self):
        return f'<BaiDuResponse(item={repr(self.item)} , url={repr(self.url)})>'


class BaiDu:
    BaiDuUpLoadURL = 'https://graph.baidu.com/upload'

    def __init__(self, **requests_kwargs):
        self.requests_kwargs = requests_kwargs
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36 Edg/89.0.774.45'
        }

    def search(self, url: str):
        if url[:4] == 'http':  # 网络url
            m = {'image': url,
                 'range': '{"page_from": "searchIndex"}',
                 'from': "pc",
                 'tn': 'pc',
                 'image_source': 'PC_UPLOAD_SEARCH_FILE',
                 'sdkParams': '{"data":"b75e75e2292710b4d9789fb5d4f425cde2213ace63b8c94aa9af6446b1b3f54438e7c1c2b4ad1cc62b35d473d70b10c031d846ab1ba8c858ab0cd0dfc7b9a109c1e709f18800034e7ec82a2c2bb5b7e8","key_id":"23","sign":"0f0bfdc2"}'
                 }
            headers = self.headers
        else:  # 文件
            m = MultipartEncoder(fields={
                'image': ('filename', open(url, 'rb'), "type=multipart/form-data"),
                'range': '{"page_from": "searchIndex"}',
                'from': "pc",
                'tn': 'pc',
                'image_source': 'PC_UPLOAD_SEARCH_FILE',
                'sdkParams': '{"data":"b75e75e2292710b4d9789fb5d4f425cde2213ace63b8c94aa9af6446b1b3f54438e7c1c2b4ad1cc62b35d473d70b10c031d846ab1ba8c858ab0cd0dfc7b9a109c1e709f18800034e7ec82a2c2bb5b7e8","key_id":"23","sign":"0f0bfdc2"}'
            })
            headers = {'Content-Type': m.content_type,
                       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36 Edg/89.0.774.45'}
        urllib3.disable_warnings()
        res = requests.post(self.BaiDuUpLoadURL, headers=headers, data=m, verify=False, **self.requests_kwargs)  # 上传文件
        url = res.json()['data']['url']
        resp = requests.get(url, headers=self.headers, verify=False, **self.requests_kwargs)
        return BaiDuResponse(resp)
