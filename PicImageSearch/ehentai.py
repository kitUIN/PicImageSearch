from pathlib import Path
from typing import Any, Dict, Optional, Union

from .model import EHentaiResponse
from .network import HandOver


class EHentai(HandOver):
    """API client for the EHentai image search engine.

    Used for performing reverse image searches using EHentai service.

    Attributes:
        covers: A flag to search only for covers.
        similar: A flag to enable similarity scanning.
        exp: A flag to include results from expunged galleries.
    """

    def __init__(
        self,
        covers: bool = False,
        similar: bool = True,
        exp: bool = False,
        **request_kwargs: Any
    ):
        """Initializes an EHentai API client with specified configurations.

        Args:
            covers: If True, search only for covers; otherwise, False.
            similar: If True, enable similarity scanning; otherwise, False.
            exp: If True, include results from expunged galleries; otherwise, False.
            **request_kwargs: Additional arguments for network requests.
        """
        super().__init__(**request_kwargs)
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
            "https://exhentai.org/upld/image_lookup.php"
            if ex
            else "https://upld.e-hentai.org/image_lookup.php"
        )
        data: Dict[str, Any] = {"f_sfile": "search"}
        if url:
            files: Dict[str, Any] = {"sfile": await self.download(url)}
        elif file:
            files = {"sfile": file if isinstance(file, bytes) else open(file, "rb")}
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
