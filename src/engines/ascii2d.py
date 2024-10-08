from pathlib import Path
from typing import Any, Optional, Union

from ..model import Ascii2DResponse
from ..utils import read_file
from .base import BaseSearchEngine


class Ascii2D(BaseSearchEngine):
    """API client for the Ascii2D image search engine.

    Used for performing reverse image searches using Ascii2D service.

    Attributes:
        base_url: The base URL for Ascii2D searches.
        bovw: A flag to use feature search over color combination search.

    Note:
        Color combination search is recommended for images similar in appearance to the original.
        Feature search is better for images with partial matches (e.g., cropped or rotated).
        Feature search may not yield accurate results with significantly different images.
    """

    def __init__(
        self,
        base_url: str = "https://ascii2d.net",
        bovw: bool = False,
        **request_kwargs: Any,
    ):
        """Initializes an Ascii2D API client with specified configurations.

        Args:
            base_url: The base URL for Ascii2D searches.
            bovw: If True, use feature search; otherwise, use color combination search.
            **request_kwargs: Additional arguments for network requests.
        """
        base_url = f"{base_url}/search"
        super().__init__(base_url, **request_kwargs)
        self.bovw = bovw

    async def search(
        self,
        url: Optional[str] = None,
        file: Union[str, bytes, Path, None] = None,
        **kwargs: Any,
    ) -> Ascii2DResponse:
        """Performs a reverse image search on Ascii2D.

        Supports searching by image URL or by uploading an image file.

        Requires either 'url' or 'file' to be provided.

        Args:
            url: URL of the image to search.
            file: Local image file (path or bytes) to search.

        Returns:
            Ascii2DResponse: Contains search results and additional information.

        Raises:
            ValueError: If neither 'url' nor 'file' is provided.
        """
        await super().search(url, file, **kwargs)

        data: Optional[dict[str, Any]] = None
        files: Optional[dict[str, Any]] = None

        if url:
            endpoint = "uri"
            data = {"uri": url}
        else:
            endpoint = "file"
            files = {"file": read_file(file)}

        resp = await self._make_request(
            method="post",
            endpoint=endpoint,
            data=data,
            files=files,
        )

        # If 'bovw' is enabled, switch to feature search mode.
        if self.bovw:
            resp = await self.get(resp.url.replace("/color/", "/bovw/"))

        return Ascii2DResponse(resp.text, resp.url)
