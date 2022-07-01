import asyncio
from typing import Any, BinaryIO, Dict, Optional, Union

from .model import TraceMoeItem, TraceMoeMe, TraceMoeResponse
from .network import HandOver

ANIME_INFO_QUERY = """
query ($id: Int) {
  Media (id: $id, type: ANIME) {
    id
    idMal
    title {
      native
      romaji
      english
    }
    type
    format
    startDate {
      year
      month
      day
    }
    endDate {
      year
      month
      day
    }
    coverImage {
      large
    }
    synonyms
    isAdult
  }
}
"""


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

    # @staticmethod
    # def _base_64(filename):
    #     with open(filename, 'rb') as f:
    #         coding = base64.b64encode(f.read())  # 读取文件内容，转换为base64编码
    #         # print('本地base64转码~')
    #         return coding.decode()

    # 获取自己的信息
    async def me(self, key: Optional[str] = None) -> TraceMoeMe:
        params = {"key": key} if key else None
        resp = await self.get(self.me_url, params=params)
        return TraceMoeMe(resp.json())

    @staticmethod
    def set_params(
        url: Optional[str],
        anilist_id: Optional[int],
        cut_borders: bool,
    ) -> Dict[str, Union[bool, int, str]]:
        params: Dict[str, Union[bool, int, str]] = {}
        if cut_borders:
            params["cutBorders"] = True
        if anilist_id:
            params["anilistID"] = anilist_id
        if url:
            params["url"] = url
        return params

    async def update_anime_info(
        self, item: TraceMoeItem, chinese_title: bool = True
    ) -> None:
        variables = {"id": item.anilist}
        url = "https://trace.moe/anilist/"
        item.anime_info = (
            await self.post(
                url=url, json={"query": ANIME_INFO_QUERY, "variables": variables}
            )
        ).json()["data"]["Media"]
        item.idMal = item.anime_info[
            "idMal"
        ]  # 匹配的MyAnimelist ID见https://myanimelist.net/
        item.title = item.anime_info["title"]
        item.title_native = item.anime_info["title"]["native"]
        item.title_romaji = item.anime_info["title"]["romaji"]
        item.title_english = item.anime_info["title"]["english"]
        item.synonyms = item.anime_info["synonyms"]
        item.isAdult = item.anime_info["isAdult"]
        item.type = item.anime_info["type"]
        item.format = item.anime_info["format"]
        item.start_date = item.anime_info["startDate"]
        item.end_date = item.anime_info["endDate"]
        item.cover_image = item.anime_info["coverImage"]["large"]
        if chinese_title:
            item.title_chinese = item.anime_info["title"].get("chinese", "")

    async def search(
        self,
        url: Optional[str] = None,
        file: Optional[BinaryIO] = None,
        key: Optional[str] = None,
        anilist_id: Optional[int] = None,
        chinese_title: bool = True,
        cut_borders: bool = True,
    ) -> TraceMoeResponse:
        """识别图片
        :param key: API密钥 https://soruly.github.io/trace.moe-api/#/limits?id=api-search-quota-and-limits
        :param url: 网络地址(http或https链接) When using video / gif, only the 1st frame would be extracted for searching
        :param file: 本地图片文件 When using video / gif, only the 1st frame would be extracted for searching
        :param anilist_id: 搜索限制为特定的 Anilist ID(默认无)
        :param chinese_title: 中文番剧标题
        :param cut_borders: 切割黑边框(默认开启)
        """
        headers = {"x-trace-key": key} if key else None
        if url:
            params = self.set_params(url, anilist_id, cut_borders)
            resp = await self.get(self.search_url, headers=headers, params=params)  # type: ignore
        elif file:
            params = self.set_params(None, anilist_id, cut_borders)
            resp = await self.post(
                self.search_url,
                headers=headers,
                params=params,
                files={"image": file},
            )
        else:
            raise ValueError("url or file is required")
        result = TraceMoeResponse(resp.json(), self.mute, self.size)
        await asyncio.gather(
            *[self.update_anime_info(item, chinese_title) for item in result.raw]
        )
        return result
