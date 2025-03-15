from pathlib import Path
from typing import Any, Optional, Union

from typing_extensions import override

from ..model import IqdbResponse
from ..utils import read_file
from .base import BaseSearchEngine


class Iqdb(BaseSearchEngine[IqdbResponse]):
    """API client for the Iqdb image search engine.

    A client implementation for performing reverse image searches using Iqdb's services.
    Supports both anime-style images (iqdb.org) and real-life images (3d.iqdb.org).

    Attributes:
        base_url (str): The base URL for Iqdb searches, determined by is_3d parameter.

    Note:
        - For anime/artwork images, uses iqdb.org
        - For real-life/3D images, uses 3d.iqdb.org
    """

    def __init__(
        self,
        is_3d: bool = False,
        **request_kwargs: Any,
    ):
        """Initializes an Iqdb API client with request configuration.

        Args:
            is_3d (bool): If True, searches on 3d.iqdb.org for real-life images; otherwise, iqdb.org for anime images.
            **request_kwargs (Any): Additional arguments for network requests.
        """
        base_url = "https://3d.iqdb.org" if is_3d else "https://iqdb.org"
        super().__init__(base_url, **request_kwargs)

    @override
    async def search(
        self,
        url: Optional[str] = None,
        file: Union[str, bytes, Path, None] = None,
        force_gray: bool = False,
        **kwargs: Any,
    ) -> IqdbResponse:
        """Performs a reverse image search on Iqdb.

        This method supports two ways of searching:
            1. Search by image URL
            2. Search by uploading a local image file

        Args:
            url (Optional[str]): URL of the image to search.
            file (Union[str, bytes, Path, None]): Local image file, can be a path string, bytes data, or Path object.
            force_gray (bool): If True, ignores color information during search, useful for
                    finding similar images with different color schemes.
            **kwargs (Any): Additional arguments passed to the parent class.

        Returns:
            IqdbResponse: An object containing:
                - Search results from various supported image databases
                - Additional metadata about the search
                - The final search URL

        Raises:
            ValueError: If neither `url` nor `file` is provided.

        Note:
            - Only one of `url` or `file` should be provided.
            - The search behavior differs based on the is_3d parameter set during initialization:
                - is_3d=False: Searches anime/artwork images on iqdb.org
                - is_3d=True: Searches real-life images on 3d.iqdb.org
            - The force_gray option can help find visually similar images regardless of coloring
        """
        data: dict[str, Any] = {}
        files: Optional[dict[str, Any]] = None

        if force_gray:
            data["forcegray"] = "on"

        if url:
            data["url"] = url
        elif file:
            files = {"file": read_file(file)}
        else:
            raise ValueError("Either 'url' or 'file' must be provided")

        resp = await self._send_request(
            method="post",
            data=data,
            files=files,
        )

        return IqdbResponse(resp.text, resp.url)
