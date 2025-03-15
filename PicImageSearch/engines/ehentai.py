from pathlib import Path
from typing import Any, Optional, Union

from typing_extensions import override

from ..model import EHentaiResponse
from ..utils import read_file
from .base import BaseSearchEngine


class EHentai(BaseSearchEngine[EHentaiResponse]):
    """API client for the EHentai image search engine.

    Used for performing reverse image searches using EHentai service.

    Attributes:
        base_url (str): The base URL for EHentai searches.
        is_ex (bool): If True, search on exhentai.org; otherwise, use e-hentai.org.
        covers (bool): A flag to search only for covers.
        similar (bool): A flag to enable similarity scanning.
        exp (bool): A flag to include results from expunged galleries.
    """

    def __init__(
        self,
        is_ex: bool = False,
        covers: bool = False,
        similar: bool = True,
        exp: bool = False,
        **request_kwargs: Any,
    ):
        """Initializes an EHentai API client with specified configurations.

        Args:
            is_ex (bool): If True, search on exhentai.org; otherwise, use e-hentai.org.
            covers (bool): If True, search only for covers; otherwise, search all images.
            similar (bool): If True, enable similarity scanning for more results.
            exp (bool): If True, include results from expunged galleries.
            **request_kwargs (Any): Additional arguments for network requests (e.g., cookies, proxies).

        Note:
            - For exhentai.org searches (is_ex=True), valid cookies must be provided in request_kwargs.
            - The base URL is automatically selected based on the is_ex parameter.
        """
        base_url = "https://upld.exhentai.org" if is_ex else "https://upld.e-hentai.org"
        super().__init__(base_url, **request_kwargs)
        self.is_ex: bool = is_ex
        self.covers: bool = covers
        self.similar: bool = similar
        self.exp: bool = exp

    @override
    async def search(
        self,
        url: Optional[str] = None,
        file: Union[str, bytes, Path, None] = None,
        **kwargs: Any,
    ) -> EHentaiResponse:
        """Performs a reverse image search on EHentai/ExHentai.

        This method supports two ways of searching:
            1. Search by image URL
            2. Search by uploading a local image file

        Args:
            url (Optional[str]): URL of the image to search.
            file (Union[str, bytes, Path, None]): Local image file, can be a path string, bytes data, or Path object.
            **kwargs (Any): Additional arguments passed to the parent class.

        Returns:
            EHentaiResponse: Contains search results and metadata, including:
                - Similar gallery entries
                - Gallery URLs and titles
                - Similarity scores
                - Additional metadata from the search results

        Raises:
            ValueError: If neither `url` nor `file` is provided.
            RuntimeError: If searching on ExHentai without proper authentication.

        Note:
            - Only one of `url` or `file` should be provided.
            - For ExHentai searches, valid cookies must be provided in the request_kwargs.
            - Search behavior is affected by the covers, similar, and exp flags set during initialization.
        """
        endpoint = "upld/image_lookup.php" if self.is_ex else "image_lookup.php"
        data: dict[str, Any] = {"f_sfile": "File Search"}

        if url:
            files = {"sfile": await self.download(url)}
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

        resp = await self._send_request(
            method="post",
            endpoint=endpoint,
            data=data,
            files=files,
        )

        return EHentaiResponse(resp.text, resp.url)
