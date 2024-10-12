from pathlib import Path
from typing import Any, Optional, Union

from ..model import IqdbResponse
from ..utils import read_file
from .base import BaseSearchEngine


class Iqdb(BaseSearchEngine):
    """API client for the Iqdb image search engine.

    Used for performing reverse image searches using Iqdb service.

    Attributes:
        base_url: The base URL for Iqdb searches.
    """

    def __init__(
        self,
        is_3d: bool = False,
        **request_kwargs: Any,
    ):
        """Initializes an Iqdb API client with request configuration.

        Args:
            is_3d: If True, searches on 3d.iqdb.org for real-life images; otherwise, iqdb.org for anime images.
            **request_kwargs: Additional arguments for network requests.
        """
        base_url = "https://3d.iqdb.org" if is_3d else "https://iqdb.org"
        super().__init__(base_url, **request_kwargs)

    async def search(
        self,
        url: Optional[str] = None,
        file: Union[str, bytes, Path, None] = None,
        force_gray: bool = False,
        **kwargs: Any,
    ) -> IqdbResponse:
        """Performs a reverse image search on Iqdb.

        Supports searching by image URL or by uploading an image file.

        Requires either 'url' or 'file' to be provided.

        Args:
            url: URL of the image to search.
            file: Local image file (path or bytes) to search.
            force_gray: If True, ignores color information in the image.

        Returns:
            IqdbResponse: Contains search results and additional information.

        Raises:
            ValueError: If neither 'url' nor 'file' is provided.

        Note:
            Search can be tailored for anime or real-life images using `is_3d` parameter.
        """
        await super().search(url, file, **kwargs)

        data: dict[str, Any] = {}
        files: Optional[dict[str, Any]] = None

        if force_gray:
            data["forcegray"] = "on"

        if url:
            data["url"] = url
        else:
            files = {"file": read_file(file)}

        resp = await self._make_request(
            method="post",
            data=data,
            files=files,
        )

        return IqdbResponse(resp.text, resp.url)
