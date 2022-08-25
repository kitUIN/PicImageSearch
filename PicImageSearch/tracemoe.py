import asyncio
from json import loads as json_loads
from pathlib import Path
from typing import Any, Dict, Optional, Union

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

        :param size: preview video/image size(can be:s/m/l)(small/medium/large)
        :param mute: mute the preview video（default:False）
        :param **request_kwargs: proxies and bypass settings.
        """
        super().__init__(**request_kwargs)
        self.size: Optional[str] = size
        self.mute: bool = mute

    # 获取自己的信息
    async def me(self, key: Optional[str] = None) -> TraceMoeMe:
        params = {"key": key} if key else None
        resp_text, _, _ = await self.get(self.me_url, params=params)
        return TraceMoeMe(json_loads(resp_text))

    @staticmethod
    def set_params(
        url: Optional[str],
        anilist_id: Optional[int],
        cut_borders: bool,
    ) -> Dict[str, Union[bool, int, str]]:
        params: Dict[str, Union[bool, int, str]] = {}
        if cut_borders:
            params["cutBorders"] = "true"
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
        item.anime_info = json_loads(
            (
                await self.post(
                    url=url, json={"query": ANIME_INFO_QUERY, "variables": variables}
                )
            )[0]
        )["data"]["Media"]
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
        file: Union[str, bytes, Path, None] = None,
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
        data: Optional[Dict[str, Any]] = None
        if url:
            params = self.set_params(url, anilist_id, cut_borders)
        elif file:
            params = self.set_params(None, anilist_id, cut_borders)
            data = (
                {"file": file}
                if isinstance(file, bytes)
                else {"file": open(file, "rb")}
            )
        else:
            raise ValueError("url or file is required")
        resp_text, _, _ = await self.post(
            self.search_url,
            headers=headers,
            params=params,
            data=data,
        )
        result = TraceMoeResponse(json_loads(resp_text), self.mute, self.size)
        await asyncio.gather(
            *[self.update_anime_info(item, chinese_title) for item in result.raw]
        )
        return result
