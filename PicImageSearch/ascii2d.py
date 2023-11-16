from pathlib import Path
from typing import Any, Optional, Union

from .model import Ascii2DResponse
from .network import HandOver


class Ascii2D(HandOver):
    """API client for the Ascii2D image search engine.

    Used for performing reverse image searches using Ascii2D service.

    Attributes:
        bovw: A flag to use feature search over color combination search.

    Note:
        Color combination search is recommended for images similar in appearance to the original.
        Feature search is better for images with partial matches (e.g., cropped or rotated).
        Feature search may not yield accurate results with significantly different images.
    """

    def __init__(self, bovw: bool = False, **request_kwargs: Any):
        """Initializes an Ascii2D API client with specified configurations.

        Args:
            bovw: If True, use feature search; otherwise, use color combination search.
            **request_kwargs: Additional arguments for network requests.
        """
        super().__init__(**request_kwargs)
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
        if url:
            ascii2d_url = "https://ascii2d.net/search/uri"
            resp = await self.post(ascii2d_url, data={"uri": url})
        elif file:
            ascii2d_url = "https://ascii2d.net/search/file"
            files = {"file": file if isinstance(file, bytes) else open(file, "rb")}
            resp = await self.post(ascii2d_url, files=files)
        else:
            raise ValueError("Either 'url' or 'file' must be provided")

        # If 'bovw' is enabled, switch to feature search mode.
        if self.bovw:
            resp = await self.get(resp.url.replace("/color/", "/bovw/"))

        return Ascii2DResponse(resp.text, resp.url)
