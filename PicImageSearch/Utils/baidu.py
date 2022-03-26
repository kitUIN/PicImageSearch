import json
import re
from typing import Any, Dict, List, Optional

from httpx import Response


class BaiDuItem:
    def __init__(self, data: Dict[str, Any]):
        self.origin: Dict[str, Any] = data  # 原始数据
        self.page_title: str = data["fromPageTitle"]  # 页面标题
        self.title: str = data["title"][0]  # 标题
        self.abstract: str = data["abstract"]  # 说明文字
        self.image_src: str = data["image_src"]  # 图片地址
        self.url: str = data["url"]  # 图片所在网页地址
        self.img_list: List[str] = data.get("imgList", [])  # 其他图片地址列表


class BaiDuResponse:
    def __init__(self, res: Response):
        self.url: str = str(res.url)  # 搜索结果地址
        self.similar: List[Dict[str, Any]] = []  # 相似结果返回值
        self.raw: List[BaiDuItem] = []  # 来源结果返回值
        # 原始数据
        self.origin: List[Dict[str, Any]] = json.loads(
            re.search(r"cardData = (.+);window\.commonData", res.text)[1]  # type: ignore
        )
        self.same: Optional[Dict[str, Any]] = {}
        for i in self.origin:
            setattr(self, i["cardName"], i)
        if self.same:
            self.raw = [BaiDuItem(x) for x in self.same["tplData"]["list"]]
            info = self.same["extData"]["showInfo"]
            del info["other_info"]
            for y in info:
                for z in info[y]:
                    try:
                        self.similar[info[y].index(z)][y] = z
                    except IndexError:
                        self.similar.append({y: z})
        # 获取所有卡片名
        self.item: List[str] = [
            attr
            for attr in dir(self)
            if not callable(getattr(self, attr))
            and not attr.startswith(("__", "origin", "raw", "same", "url"))
        ]
