from pathlib import Path
from typing import Any, Optional, Union

from .model import Ascii2DResponse
from .network import HandOver
from .utils import read_file


class Ascii2D(HandOver):
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
        super().__init__(**request_kwargs)
        self.base_url = f"{base_url}/search"
        self.bovw = bovw

    async def search(
        self, url: Optional[str] = None, file: Union[str, bytes, Path, None] = None
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
        _url = f"{self.base_url}/uri" if url else f"{self.base_url}/file"
        if url:
            resp = await self.post(_url, data={"uri": url})
        elif file:
            files = {"file": read_file(file)}
            resp = await self.post(_url, files=files)
        else:
            raise ValueError("Either 'url' or 'file' must be provided")

        # If 'bovw' is enabled, switch to feature search mode.
        if self.bovw:
            resp = await self.get(resp.url.replace("/color/", "/bovw/"))

        return Ascii2DResponse(resp.text, resp.url)
