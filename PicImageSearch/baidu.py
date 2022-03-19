from .network import HandOver
from .Utils import BaiDuResponse


class BaiDu(HandOver):
    def __init__(self, **requests_kwargs):
        super().__init__(**requests_kwargs)
        self.url: str = "https://graph.baidu.com/upload"
        self.requests_kwargs: dict = requests_kwargs

    async def search(self, url: str) -> BaiDuResponse:
        params = {"from": "pc"}
        files = None
        if url[:4] == "http":  # 网络url
            params["image"] = url
        else:
            # 上传文件
            files = {"image": open(url, "rb")}
        res = await self.post(self.url, _params=params, _files=files)
        res = await self.get(res.json()["data"]["url"])
        return BaiDuResponse(res)
