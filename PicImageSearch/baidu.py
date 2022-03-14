import time

import requests
from PicImageSearch.Utils import BaiDuResponse
from requests_toolbelt import MultipartEncoder


class BaiDu:
    def __init__(self, **requests_kwargs):
        self.url = "https://graph.baidu.com/upload"
        self.requests_kwargs = requests_kwargs
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36 Edg/89.0.774.45"
        }

    def search(self, url: str) -> BaiDuResponse:
        params = {"uptime": int(time.time())}
        if url[:4] == "http":  # 网络url
            m = {
                "image": url,
                "range": '{"page_from": "searchIndex"}',
                "from": "pc",
                "tn": "pc",
                "image_source": "PC_UPLOAD_MOVE",
                "sdkParams": '{"data":"a4388c3ef696d354e7f05402e1d38daf48bfb4f3d5bd941e2d0c920dc3b387065b7c85440986897b1f56ef6d352e3b94b3ea435ba5e1bb5a86c5feb88e2e9e1179abd5b8699370b6be8e7cfb96e6e605","key_id":"23","sign":"f22953e8"}',
            }
            headers = self.headers
        else:  # 文件
            m = MultipartEncoder(
                fields={
                    "image": ("filename", open(url, "rb"), "type=multipart/form-data"),
                    "range": '{"page_from": "searchIndex"}',
                    "from": "pc",
                    "tn": "pc",
                    "image_source": "PC_UPLOAD_SEARCH_FILE",
                    "sdkParams": '{"data":"a4388c3ef696d354e7f05402e1d38daf48bfb4f3d5bd941e2d0c920dc3b387065b7c85440986897b1f56ef6d352e3b94b3ea435ba5e1bb5a86c5feb88e2e9e1179abd5b8699370b6be8e7cfb96e6e605","key_id":"23","sign":"f22953e8"}',
                }
            )
            headers = {
                "Content-Type": m.content_type,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36 Edg/89.0.774.45",
            }
        res = requests.post(
            self.url,
            headers=headers,
            params=params,
            data=m,
            verify=False,
            **self.requests_kwargs
        )  # 上传文件

        url = res.json()["data"]["url"]
        print(url)
        resp = requests.get(
            url, headers=self.headers, verify=False, **self.requests_kwargs
        )
        print(resp.text)
        return BaiDuResponse(resp)
