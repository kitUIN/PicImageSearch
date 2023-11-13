from pathlib import Path
from typing import Any, Dict, Optional, Union

from .model import IqdbResponse
from .network import HandOver


class Iqdb(HandOver):
    """API client for the Iqdb image search engine.

    Attributes:
        url: The URL endpoint for the Iqdb API.
        params: Query parameters for the Iqdb API.
    """

    def __init__(self, **request_kwargs: Any):
        """Initializes Iqdb API client with configuration.

        Args:
            **request_kwargs: Additional keyword arguments for request configuration.
        """
        super().__init__(**request_kwargs)

    async def search(
        self,
        url: Optional[str] = None,
        file: Union[str, bytes, Path, None] = None,
        force_gray: bool = False,
        is_3d: bool = False,
    ) -> IqdbResponse:
        """Performs a reverse image search on Iqdb using the URL or file of the image.

        The user must provide either a URL or a file.

        Args:
            url: URL of the image to search.
            file: Image file to search. Can be a file path (str or Path) or raw bytes.
            force_gray: Whether to ignore color.
            is_3d: Whether to search for irl images on none anime related sites. This uses the 3d.iqdb.org endpoint.

        Returns:
            An instance of IqdbResponse containing the search results and additional metadata.

        Raises:
            ValueError: If neither `url` nor `file` is provided.
        """
        iqdb_url = "https://3d.iqdb.org/" if is_3d else "https://iqdb.org/"
        data: Dict[str, Any] = {}
        if force_gray:  # 忽略颜色
            data["forcegray"] = "on"
        if url:
            data["url"] = url
            resp = await self.post(iqdb_url, data=data)
        elif file:
            files = {"file": file if isinstance(file, bytes) else open(file, "rb")}
            resp = await self.post(iqdb_url, data=data, files=files)
        else:
            raise ValueError("url or file is required")
        return IqdbResponse(resp.text)
