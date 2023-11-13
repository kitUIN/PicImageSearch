from pathlib import Path
from typing import Any, Dict, Optional, Union

from .model import EHentaiResponse
from .network import HandOver


class EHentai(HandOver):
    """API client for the EHentai image search engine.

    Attributes:
        url: The URL endpoint for the EHentai API.
        params: Query parameters for the EHentai API.
    """

    def __init__(
        self,
        covers: bool = False,
        similar: bool = True,
        exp: bool = False,
        **request_kwargs: Any
    ):
        """Initializes EHentai API client with configuration.

        Args:
            covers: Whether to only search for covers.
            similar: Whether to use similarity scan to find similar images.
            exp: Whether to include results from the expunged galleries.
            **request_kwargs: Additional keyword arguments for request configuration.
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
        """Performs a reverse image search on EHentai using the URL or file of the image.

        The user must provide either a URL or a file.

        Note:
            To use `ex` you must be logged in to exhentai.org via the cookies defined in `EHentai.request_kwargs`.
            We recommend using `ex=bool(cookies)` or something similar to determine whether to use `ex`.

        Args:
            url: URL of the image to search.
            file: Image file to search. Can be a file path (str or Path) or raw bytes.
            ex: Whether to search on exhentai.org instead of e-hentai.org. Defaults to False.

        Returns:
            An instance of EHentaiResponse containing the search results and additional metadata.

        Raises:
            ValueError: If neither `url` nor `file` is provided.
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
            raise ValueError("url or file is required")
        if self.covers:
            data["fs_covers"] = "on"
        if self.similar:
            data["fs_similar"] = "on"
        if self.exp:
            data["fs_exp"] = "on"
        resp = await self.post(url=_url, data=data, files=files)
        return EHentaiResponse(resp.text, resp.url)
