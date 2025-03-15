from json import loads as json_loads
from pathlib import Path
from typing import Any, Optional, Union

from httpx import QueryParams
from typing_extensions import override

from ..model import SauceNAOResponse
from ..utils import read_file
from .base import BaseSearchEngine


class SauceNAO(BaseSearchEngine[SauceNAOResponse]):
    """API client for the SauceNAO image search engine.

    Used for performing reverse image searches using SauceNAO service.

    Attributes:
        base_url (str): The base URL for SauceNAO searches.
        params (dict[str, Any]): The query parameters for SauceNAO search.
    """

    def __init__(
        self,
        base_url: str = "https://saucenao.com",
        api_key: Optional[str] = None,
        numres: int = 5,
        hide: int = 0,
        minsim: int = 30,
        output_type: int = 2,
        testmode: int = 0,
        dbmask: Optional[int] = None,
        dbmaski: Optional[int] = None,
        db: int = 999,
        dbs: Optional[list[int]] = None,
        **request_kwargs: Any,
    ):
        """Initializes a SauceNAO API client with specified configurations.

        Args:
            base_url (str): The base URL for SauceNAO searches, defaults to 'https://saucenao.com'.
            api_key (Optional[str]): API key for SauceNAO API access, required for full API functionality.
            numres (int): Number of results to return (1-40), defaults to 5.
            hide (int): Content filtering level (0-3), defaults to 0.
                0: Show all results
                1: Hide expected explicit results
                2: Hide expected questionable results
                3: Hide all but expected safe results
            minsim (int): Minimum similarity percentage for results (0-100), defaults to 30.
            output_type (int): Output format of search results, defaults to 2.
                0: HTML
                1: XML
                2: JSON
            testmode (int): If 1, performs a dry-run search without using search quota.
            dbmask (Optional[int]): Bitmask for enabling specific databases.
            dbmaski (Optional[int]): Bitmask for disabling specific databases.
            db (int): Database index to search from (0-999), defaults to 999 (all databases).
            dbs (Optional[list[int]]): List of specific database indices to search from.
            **request_kwargs (Any): Additional arguments passed to the HTTP client.

        Note:
            - API documentation: https://saucenao.com/user.php?page=search-api
            - Database indices: https://saucenao.com/tools/examples/api/index_details.txt
            - Using API key is recommended to avoid rate limits and access more features.
            - When `dbs` is provided, it takes precedence over `db` parameter.
        """
        base_url = f"{base_url}/search.php"
        super().__init__(base_url, **request_kwargs)
        params: dict[str, Any] = {
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
        self.params: QueryParams = QueryParams(params)
        if dbs is not None:
            self.params = self.params.remove("db")
            for i in dbs:
                self.params = self.params.add("dbs[]", i)

    @override
    async def search(
        self,
        url: Optional[str] = None,
        file: Union[str, bytes, Path, None] = None,
        **kwargs: Any,
    ) -> SauceNAOResponse:
        """Performs a reverse image search on SauceNAO.

        This method supports two ways of searching:
            1. Search by image URL
            2. Search by uploading a local image file

        Args:
            url (Optional[str]): URL of the image to search.
            file (Union[str, bytes, Path, None]): Local image file, can be a path string, bytes data, or Path object.
            **kwargs (Any): Additional arguments passed to the parent class.

        Returns:
            SauceNAOResponse: An object containing:
                - Search results with similarity scores
                - Source information and thumbnails
                - Additional metadata (status code, search quotas)

        Raises:
            ValueError: If neither `url` nor `file` is provided.

        Note:
            - Only one of `url` or `file` should be provided.
            - API limits vary based on account type and API key usage.
            - Free accounts are limited to:
                * 150 searches per day
                * 4 searches per 30 seconds
            - Results are sorted by similarity score in descending order.
        """
        params = self.params
        files: Optional[dict[str, Any]] = None

        if url:
            params = params.add("url", url)
        elif file:
            files = {"file": read_file(file)}
        else:
            raise ValueError("Either 'url' or 'file' must be provided")

        resp = await self._send_request(
            method="post",
            params=params,
            files=files,
        )

        resp_json = json_loads(resp.text)
        resp_json.update({"status_code": resp.status_code})

        return SauceNAOResponse(resp_json, resp.url)
