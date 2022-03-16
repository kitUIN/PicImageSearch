from PicImageSearch.Utils import BaiDuResponse

from .network import HandOver


class AsyncBaiDu(HandOver):
    def __init__(self, **requests_kwargs):
        super().__init__(**requests_kwargs)
        self.url = "https://graph.baidu.com/upload"
        self.requests_kwargs = requests_kwargs

    async def search(self, url: str) -> BaiDuResponse:
        params = {"from": "pc"}
        files = None
        if url[:4] == "http":  # 网络url
            params["image"] = url
        else:
            # 上传文件
            files = {"image": open(url, "rb")}
        res = await self.post(self.url, _params=params, _files=files)
        url = res.json()["data"]["url"]
        res = await self.get(url)
        return BaiDuResponse(res)
