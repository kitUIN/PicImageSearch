from loguru import logger

from .network import HandOver
from .Utils import TraceMoeMe, TraceMoeResponse, get_error_message


class TraceMoe(HandOver):
    search_url = "https://api.trace.moe/search"
    me_url = "https://api.trace.moe/me"

    def __init__(self, mute=False, size=None, **requests_kwargs):
        """主类

        :param size: 预览 视频/图像 大小(可填:s/m/l)(小/中/大)
        :param mute: 预览视频是否静音（默认不静音）
        :param requests_kwargs:代理设置
        """
        super().__init__(**requests_kwargs)
        self.size: str = size
        self.mute: bool = mute
        self.requests_kwargs = requests_kwargs

    # @staticmethod
    # def _base_64(filename):
    #     with open(filename, 'rb') as f:
    #         coding = base64.b64encode(f.read())  # 读取文件内容，转换为base64编码
    #         # print('本地base64转码~')
    #         return coding.decode()

    async def me(self, key=None) -> TraceMoeMe:
        """获取自己的信息"""
        try:
            params = None
            if key:
                params = {"key": key}
            res = await self.get(self.me_url, _params=params, **self.requests_kwargs)
            if res.status_code == 200:
                data = res.json()
                return TraceMoeMe(data)
            else:
                logger.error(res.status_code)
        except Exception as e:
            logger.info(e)

    @staticmethod
    def _first_if(param):
        if param != "":
            param += "&"
        return param

    @staticmethod
    def set_params(url, anilist_id, anilist_info, cut_borders):
        params = {}
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
        url,
        key=None,
        anilist_id=None,
        chinese_title=True,
        anilist_info=True,
        cut_borders=True,
    ) -> TraceMoeResponse:
        """识别图片

        :param key: API密钥 https://soruly.github.io/trace.moe-api/#/limits?id=api-search-quota-and-limits
        :param url: 网络地址(http或https链接)或本地(本地图片路径)  When using video / gif, only the 1st frame would be extracted for searching.
        :param anilist_id: 搜索限制为特定的 Anilist ID(默认无)
        :param anilist_info: 详细信息(默认开启)
        :param chinese_title: 中文番剧标题
        :param cut_borders: 切割黑边框(默认开启)
        """
        try:
            headers = None
            if headers:
                headers = {"x-trace-key": key}
            if url[:4] == "http":  # 网络url
                params = self.set_params(url, anilist_id, anilist_info, cut_borders)
                res = await self.get(self.search_url, _headers=headers, _params=params)
            else:  # 是否是本地文件
                params = self.set_params(None, anilist_id, anilist_info, cut_borders)
                res = await self.post(
                    self.search_url,
                    _headers=headers,
                    _params=params,
                    _files={"image": open(url, "rb")},
                )
            if res.status_code == 200:
                data = res.json()
                return TraceMoeResponse(
                    data, chinese_title, self.mute, self.size, **self.requests_kwargs
                )
            else:
                logger.error(get_error_message(res.status_code))
        except Exception as e:
            logger.info(e)
