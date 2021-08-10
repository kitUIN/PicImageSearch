import json
import re


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
    def __init__(self, resp):
        self.url: str = resp.request.url  # 搜索结果地址
        self.similar = list()
        self.raw = list()
        self.origin: list = json.loads(re.search(pattern='cardData = (.+);window\.commonData', string=resp.text)[1])
        for i in self.origin:
            setattr(self, i['cardName'], i)
        if hasattr(self, 'same'):
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