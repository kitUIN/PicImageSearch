from json import loads as json_loads
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from httpx import QueryParams

from .model import SauceNAOResponse
from .network import HandOver


class SauceNAO(HandOver):
    """API client for the SauceNAO image search engine.

    Attributes:
        url: The URL endpoint for the SauceNAO API.
        params: Query parameters for the SauceNAO API.
    """

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
        **request_kwargs: Any,
    ):
        """Initializes SauceNAO API client with configuration.

        Further documentation on the API can be found at on saucenao.com when your account is logged in:
            https://saucenao.com/user.php?page=search-api

        For more information on `dbmask`, `dbmaski`, `db`, and `dbs` specifically, see:
            https://saucenao.com/tools/examples/api/index_details.txt

        Args:
            api_key: Access key for SauceNAO.
            numres: The number of results to return.
            hide: Control over hiding results based on content rating.
            minsim: The minimum similarity threshold required for a result.
            output_type: Specifies the output format (0=html, 1=xml, 2=json).
            testmode: Enables test mode, which performs a dry-run.
            dbmask: A bitmask to select specific indices to be enabled.
            dbmaski: A bitmask to select specific indices to be disabled.
            db: Specifies individual database indices to search (999 for all).
            dbs: Specifies multiple database indices to search.
            **request_kwargs: Additional keyword arguments for request configuration.
        """
        # minsim 控制最小相似度 (minsim controls the minimum similarity)
        super().__init__(**request_kwargs)
        self.url = "https://saucenao.com/search.php"
        params: Dict[str, Any] = {
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
        self.params = QueryParams(params)
        if dbs is not None:
            self.params = self.params.remove("db")
            for i in dbs:
                self.params = self.params.add("dbs[]", i)

    async def search(
        self, url: Optional[str] = None, file: Union[str, bytes, Path, None] = None
    ) -> SauceNAOResponse:
        """Searches for images using the SauceNAO API.

        Args:
            url: The URL of the image to be searched.
            file: The local file path or image file bytes to be searched.

        Returns:
            SauceNAOResponse: The response containing search results and metadata.

        Raises:
            ValueError: If neither a URL nor a file is provided as a search parameter.
        """
        params = self.params
        files: Optional[Dict[str, Any]] = None
        if url:
            params = params.add("url", url)
        elif file:
            files = (
                {"file": file}
                if isinstance(file, bytes)
                else {"file": open(file, "rb")}
            )
        else:
            raise ValueError("url or file is required")
        resp = await self.post(self.url, params=params, files=files)
        resp_json = json_loads(resp.text)
        resp_json.update({"status_code": resp.status_code})
        return SauceNAOResponse(resp_json)
