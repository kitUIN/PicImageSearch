from pathlib import Path
from typing import Any, Optional, Union

from .model import EHentaiResponse
from .network import HandOver
from .utils import read_file


class EHentai(HandOver):
    """API client for the EHentai image search engine.

    Used for performing reverse image searches using EHentai service.

    Attributes:
        base_url: The base URL for EHentai searches.
        base_url_ex: The base URL for EXHentai searches.
        covers: A flag to search only for covers.
        similar: A flag to enable similarity scanning.
        exp: A flag to include results from expunged galleries.
    """

    def __init__(
        self,
        base_url: str = "https://upld.e-hentai.org",
        base_url_ex: str = "https://upld.exhentai.org",
        covers: bool = False,
        similar: bool = True,
        exp: bool = False,
        **request_kwargs: Any,
    ):
        """Initializes an EHentai API client with specified configurations.

        Args:
            base_url: The base URL for EHentai searches.
            base_url_ex: The base URL for EXHentai searches.
            covers: If True, search only for covers; otherwise, False.
            similar: If True, enable similarity scanning; otherwise, False.
            exp: If True, include results from expunged galleries; otherwise, False.
            **request_kwargs: Additional arguments for network requests.
        """
        super().__init__(**request_kwargs)
        self.base_url = base_url
        self.base_url_ex = base_url_ex
        self.covers: bool = covers
        self.similar: bool = similar
        self.exp: bool = exp

    async def search(
        self,
        url: Optional[str] = None,
        file: Union[str, bytes, Path, None] = None,
        ex: bool = False,
    ) -> EHentaiResponse:
        """Performs a reverse image search on EHentai.

        Supports searching by image URL or by uploading an image file.

        Requires either 'url' or 'file' to be provided.

        Args:
            url: URL of the image to search.
            file: Local image file (path or bytes) to search.
            ex: If True, search on exhentai.org; otherwise, use e-hentai.org.

        Returns:
            EHentaiResponse: Contains search results and additional information.

        Raises:
            ValueError: If neither 'url' nor 'file' is provided.

        Note:
            Searching on exhentai.org requires logged-in status via cookies in `EHentai.request_kwargs`.
        """
        _url: str = (
            f"{self.base_url_ex}/upld/image_lookup.php"
            if ex
            else f"{self.base_url}/image_lookup.php"
        )
        data: dict[str, Any] = {"f_sfile": "File Search"}
        if url:
            files: dict[str, Any] = {"sfile": await self.download(url)}
        elif file:
            files = {"sfile": read_file(file)}
        else:
            raise ValueError("Either 'url' or 'file' must be provided")
        if self.covers:
            data["fs_covers"] = "on"
        if self.similar:
            data["fs_similar"] = "on"
        if self.exp:
            data["fs_exp"] = "on"
        resp = await self.post(url=_url, data=data, files=files)
        return EHentaiResponse(resp.text, resp.url)
