from typing import Any, Dict, Optional, Union

from .model import SauceNAOResponse
from .network import HandOver


class SauceNAO(HandOver):
    def __init__(
        self,
        api_key: Optional[str] = None,
        numres: int = 5,
        hide: int = 1,
        minsim: int = 30,
        output_type: int = 2,
        testmode: int = 0,
        dbmask: Optional[int] = None,
        dbmaski: Optional[int] = None,
        db: int = 999,
        **request_kwargs: Any
    ):
        """
        SauceNAO
        -----------
        Reverse image from https://saucenao.com\n


        Params Keys
        -----------
        :param api_key: (str) Access key for SauceNAO (default=None)
        :param output_type: (int) 0=normal (default) html 1=xml api (not implemented) 2=json api default=2
        :param testmode: (int) Test mode 0=normal 1=test (default=0)
        :param numres: (int) output number (default=5)
        :param dbmask: (int) The mask used to select the specific index to be enabled (default=None)
        :param dbmaski: (int) is used to select the mask of the specific index to be disabled (default=None)
        :param db: (int) Search for a specific index number or all indexes (default=999), see https://saucenao.com/tools/examples/api/index_details.txt
        :param minsim: (int) Control the minimum similarity (default=30)
        :param hide: (int) result hiding control, none=0, clear return value (default)=1, suspect return value=2, all return value=3
        """
        # minsim 控制最小相似度
        super().__init__(**request_kwargs)
        self.url = "https://saucenao.com/search.php"
        params: Dict[str, Union[str, int]] = {
            "testmode": testmode,
            "numres": numres,
            "output_type": output_type,
            "hide": hide,
            "db": db,
            "minsim": minsim,
        }
        if api_key is not None:
            params["api_key"] = api_key
        if dbmask is not None:
            params["dbmask"] = dbmask
        if dbmaski is not None:
            params["dbmaski"] = dbmaski
        self.params = params

    async def search(self, url: str) -> SauceNAOResponse:
        """
        SauceNAO
        -----------
        Reverse image from https://saucenao.com\n


        Return Attributes
        -----------
        • .origin = Raw data from scrapper\n
        • .raw = Simplified data from scrapper\n
        • .raw[0] = First index of simplified data that was found\n
        • .raw[0].title = First index of title that was found\n
        • .raw[0].url = First index of url source that was found\n
        • .raw[0].thumbnail = First index of url image that was found\n
        • .raw[0].similarity = First index of similarity image that was found\n
        • .raw[0].author = First index of author image that was found\n
        • .raw[0].pixiv_id = First index of pixiv id that was found\n
        • .raw[0].member_id = First index of memeber id that was found\n
        • .long_remaining = Available limmits API in a day <day limit>\n
        • .short_remaining = Available limmits API in a day <day limit>\n


        Params Keys
        -----------
        :param url: network address or local

        further documentation visit https://saucenao.com/user.php?page=search-api
        """
        params = self.params
        files = None
        if url[:4] == "http":  # 网络url
            params["url"] = url
        else:
            # 上传文件
            files = {"file": open(url, "rb")}
        resp = await self.post(
            self.url,
            params=params,
            files=files,
        )
        return SauceNAOResponse(resp.json())
