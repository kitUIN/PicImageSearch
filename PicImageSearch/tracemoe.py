from typing import Any, Dict, Optional, Union

from .model import TraceMoeMe, TraceMoeResponse
from .network import HandOver


class TraceMoe(HandOver):
    search_url = "https://api.trace.moe/search"
    me_url = "https://api.trace.moe/me"

    def __init__(
        self, mute: bool = False, size: Optional[str] = None, **request_kwargs: Any
    ):
        """主类

        :param size: 预览 视频/图像 大小(可填:s/m/l)(小/中/大)
        :param mute: 预览视频是否静音（默认不静音）
        :param request_kwargs:代理设置
        """
        super().__init__(**request_kwargs)
        self.size: Optional[str] = size
        self.mute: bool = mute
        self.request_kwargs: Dict[str, Any] = request_kwargs if request_kwargs else {}

    # @staticmethod
    # def _base_64(filename):
    #     with open(filename, 'rb') as f:
    #         coding = base64.b64encode(f.read())  # 读取文件内容，转换为base64编码
    #         # print('本地base64转码~')
    #         return coding.decode()

    # 获取自己的信息
    async def me(self, key: Optional[str] = None) -> TraceMoeMe:
        params = {"key": key} if key else None
        resp = await self.get(self.me_url, params=params, **self.request_kwargs)
        return TraceMoeMe(resp.json())

    @staticmethod
    def set_params(
        url: Optional[str],
        anilist_id: Optional[int],
        anilist_info: bool,
        cut_borders: bool,
    ) -> Dict[str, Union[bool, int, str]]:
        params: Dict[str, Union[bool, int, str]] = {}
        if anilist_info:
            params["anilistInfo"] = True
        if cut_borders:
            params["cutBorders"] = True
        if anilist_id:
            params["anilistID"] = anilist_id
        if url:
            params["url"] = url
        return params

    async def search(
        self,
        url: str,
        key: Optional[str] = None,
        anilist_id: Optional[int] = None,
        chinese_title: bool = True,
        anilist_info: bool = True,
        cut_borders: bool = True,
    ) -> TraceMoeResponse:
        """识别图片
        :param key: API密钥 https://soruly.github.io/trace.moe-api/#/limits?id=api-search-quota-and-limits
        :param url: 网络地址(http或https链接)或本地(本地图片路径)  When using video / gif, only the 1st frame would be extracted for searching
        :param anilist_id: 搜索限制为特定的 Anilist ID(默认无)
        :param anilist_info: 详细信息(默认开启)
        :param chinese_title: 中文番剧标题
        :param cut_borders: 切割黑边框(默认开启)
        """
        headers = {"x-trace-key": key} if key else None
        if url[:4] == "http":  # 网络url
            params = self.set_params(url, anilist_id, anilist_info, cut_borders)
            resp = await self.get(self.search_url, headers=headers, params=params)  # type: ignore
        else:  # 本地文件
            params = self.set_params(None, anilist_id, anilist_info, cut_borders)
            resp = await self.post(
                self.search_url,
                headers=headers,
                params=params,
                files={"image": open(url, "rb")},
            )
        return TraceMoeResponse(
            resp.json(), chinese_title, self.mute, self.size, **self.request_kwargs
        )
