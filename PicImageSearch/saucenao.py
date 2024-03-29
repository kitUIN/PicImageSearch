from json import loads as json_loads
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from httpx import QueryParams

from .model import SauceNAOResponse
from .network import HandOver

BASE_URL = "https://saucenao.com/search.php"


class SauceNAO(HandOver):
    """API client for the SauceNAO image search engine.

    Used for performing reverse image searches using SauceNAO service.

    Attributes:
        params: The query parameters for SauceNAO search.
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
        """Initializes a SauceNAO API client with specified configurations.

        Args:
            api_key: API key for SauceNAO API access.
            numres: Number of results to return from search.
            hide: Option to hide results based on content rating.
            minsim: Minimum similarity percentage for results.
            output_type: Output format of search results.
            testmode: If 1, performs a dry-run search.
            dbmask: Bitmask for enabling specific databases.
            dbmaski: Bitmask for disabling specific databases.
            db: Specifies database index(es) for search.
            dbs: List of database indices for search.
            **request_kwargs: Additional arguments for network requests.

        Note:
            Detailed API documentation is available at:
            https://saucenao.com/user.php?page=search-api (requires login).
            For specific details on `dbmask`, `dbmaski`, `db`, and `dbs`, refer to:
            https://saucenao.com/tools/examples/api/index_details.txt
        """
        super().__init__(**request_kwargs)
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
        """Performs a reverse image search on SauceNAO.

        Supports searching by image URL or by uploading an image file.

        Requires either 'url' or 'file' to be provided.

        Args:
            url: URL of the image to search.
            file: Local image file (path or bytes) to search.

        Returns:
            SauceNAOResponse: Contains search results and additional information.

        Raises:
            ValueError: If neither 'url' nor 'file' is provided.
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
            raise ValueError("Either 'url' or 'file' must be provided")
        resp = await self.post(BASE_URL, params=params, files=files)
        resp_json = json_loads(resp.text)
        resp_json.update({"status_code": resp.status_code})
        return SauceNAOResponse(resp_json)
