from typing import Any, Dict, List


class BaiDuItem:
    def __init__(self, data: Dict[str, Any]):
        self.origin: Dict[str, Any] = data  # 原始数据
        self.similarity: float = round(float(data["simi"]) * 100, 2)
        self.title: str = data["fromPageTitle"]  # 页面标题
        self.thumbnail: str = data["thumbUrl"]  # 图片地址
        self.url: str = data["fromUrl"]  # 图片所在网页地址


class BaiDuResponse:
    def __init__(self, resp_json: Dict[str, Any], resp_url: str):
        self.url: str = resp_url  # 搜索结果地址
        self.origin: Dict[str, Any] = resp_json  # 原始数据
        # 来源结果返回值
        self.raw: List[BaiDuItem] = [BaiDuItem(i) for i in resp_json["data"]["list"]]
