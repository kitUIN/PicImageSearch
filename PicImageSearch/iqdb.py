from pathlib import Path
from typing import Any, Optional, Union

from .model import IqdbResponse
from .network import HandOver
from .utils import read_file


class Iqdb(HandOver):
    """API client for the Iqdb image search engine.

    Used for performing reverse image searches using Iqdb service.

    Attributes:
        base_url: The base URL for Iqdb searches.
        base_url_3d: The base URL for Iqdb 3D searches.
    """

    def __init__(
        self,
        base_url: str = "https://iqdb.org",
        base_url_3d: str = "https://3d.iqdb.org",
        **request_kwargs: Any
    ):
        """Initializes an Iqdb API client with request configuration.

        Args:
            base_url: The base URL for Iqdb searches.
            base_url_3d: The base URL for Iqdb 3D searches.
            **request_kwargs: Additional arguments for network requests.
        """
        super().__init__(**request_kwargs)
        self.base_url = base_url
        self.base_url_3d = base_url_3d

    async def search(
        self,
        url: Optional[str] = None,
        file: Union[str, bytes, Path, None] = None,
        force_gray: bool = False,
        is_3d: bool = False,
    ) -> IqdbResponse:
        """Performs a reverse image search on Iqdb.

        Supports searching by image URL or by uploading an image file.

        Requires either 'url' or 'file' to be provided.

        Args:
            url: URL of the image to search.
            file: Local image file (path or bytes) to search.
            force_gray: If True, ignores color information in the image.
            is_3d: If True, searches on 3d.iqdb.org for real-life images; otherwise, iqdb.org for anime images.

        Returns:
            IqdbResponse: Contains search results and additional information.

        Raises:
            ValueError: If neither 'url' nor 'file' is provided.

        Note:
            Search can be tailored for anime or real-life images using `is_3d` parameter.
        """
        iqdb_url = self.base_url_3d if is_3d else self.base_url
        data: dict[str, Any] = {}
        if force_gray:
            data["forcegray"] = "on"
        if url:
            data["url"] = url
            resp = await self.post(iqdb_url, data=data)
        elif file:
            files = {"file": read_file(file)}
            resp = await self.post(iqdb_url, data=data, files=files)
        else:
            raise ValueError("Either 'url' or 'file' must be provided")
        return IqdbResponse(resp.text)
