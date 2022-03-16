import json
import re
from typing import List, Optional


class BaiDuNorm:
    def __init__(self, data):
        self.origin: dict = data
        """原始返回值"""
        self.page_title: str = data["fromPageTitle"]
        """页面标题"""
        self.title: str = data["title"][0]
        """标题"""
        self.abstract: str = data["abstract"]
        """说明文字"""
        self.image_src: str = data["image_src"]
        """图片地址"""
        self.url: str = data["url"]
        """图片所在网页地址"""
        self.img: list = list()
        """其他图片地址列表"""
        if "imgList" in data:
            self.img: list = data["imgList"]

    def __repr__(self):
        return f"<NormSauce(title={repr(self.title)})>"


class BaiDuResponse:
    def __init__(self, res):
        self.url: str = res.request.url  # 搜索结果地址
        """百度识图原网页"""
        self.similar = list()
        """相似结果返回值"""
        self.raw: Optional[List[BaiDuNorm]] = list()
        """来源结果返回值"""
        self.origin: list = json.loads(
            re.search(pattern=r"cardData = (.+);window\.commonData", string=res.text)[1]
        )
        """原始返回值"""
        for i in self.origin:
            setattr(self, i["cardName"], i)
        if hasattr(self, "same"):
            self.raw = [BaiDuNorm(x) for x in self.same["tplData"]["list"]]
            info = self.same["extData"]["showInfo"]
            for y in info:
                if y == "other_info":
                    continue
                for z in info[y]:
                    try:
                        self.similar[info[y].index(z)][y] = z
                    except:
                        self.similar.append({y: z})
        self.item = [
            attr
            for attr in dir(self)
            if not callable(getattr(self, attr))
            and not attr.startswith(("__", "origin", "raw", "same", "url"))
        ]
        """获取所有卡片名"""

    def __repr__(self):
        return f"<BaiDuResponse(item={repr(self.item)} , url={repr(self.url)})>"
