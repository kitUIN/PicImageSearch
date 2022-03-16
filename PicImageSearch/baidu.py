import httpx
from PicImageSearch.Utils import BaiDuResponse


class BaiDu:
    def __init__(self, **requests_kwargs):
        self.url = "https://graph.baidu.com/upload"
        self.requests_kwargs = requests_kwargs

    def search(self, url: str) -> BaiDuResponse:
        params = {"from": "pc"}
        files = None
        if url[:4] == "http":  # 网络url
            params["image"] = url
        else:
            # 上传文件
            files = {"image": open(url, "rb")}
        res = httpx.post(
            self.url, params=params, files=files, verify=False, **self.requests_kwargs
        )

        url = res.json()["data"]["url"]
        res = httpx.get(url, verify=False, **self.requests_kwargs)
        return BaiDuResponse(res)
