from json import loads as json_loads
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from multidict import MultiDict

from .model import SauceNAOResponse
from .network import HandOver


class SauceNAO(HandOver):
    def __init__(
        self,
        api_key: Optional[str] = None,
        numres: int = 5,
        hide: int = 0,
        minsim: int = 30,
        output_type: int = 2,
        testmode: int = 0,
        dbmask: Optional[int] = None,
        dbmaski: Optional[int] = None,
        db: int = 999,
        dbs: Optional[List[int]] = None,
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
        :param db: (int) Search for a specific index number or all indexes (default=999),
                   see https://saucenao.com/tools/examples/api/index_details.txt
        :param dbs: (list) Search for specific indexes number or all indexes (default=None),
                    see https://saucenao.com/tools/examples/api/index_details.txt
        :param minsim: (int) Control the minimum similarity (default=30)
        :param hide: (int) result hiding control, 0=show all, 1=hide expected explicit,
                     2=hide expected and suspected explicit, 3=hide all but expected safe. Default is 0.
        :param **request_kwargs: proxies and bypass settings.
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
        self.params = MultiDict(params)
        if dbs is not None:
            del self.params["db"]
            for i in dbs:
                self.params.add("dbs[]", i)

    async def search(
        self, url: Optional[str] = None, file: Union[str, bytes, Path, None] = None
    ) -> SauceNAOResponse:
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
        :param url: network address
        :param file: local file

        further documentation visit https://saucenao.com/user.php?page=search-api
        """
        params = self.params
        data: Optional[Dict[str, Any]] = None
        if url:
            params.add("url", url)
        elif file:
            data = (
                {"file": file}
                if isinstance(file, bytes)
                else {"file": open(file, "rb")}
            )
        else:
            raise ValueError("url or file is required")
        resp_text, _, resp_status = await self.post(
            self.url,
            params=params,
            data=data,
        )
        resp_json = json_loads(resp_text)
        resp_json.update({"status_code": resp_status})
        return SauceNAOResponse(resp_json)
