from pathlib import Path
from typing import Any, Optional, Union

from ..model import Ascii2DResponse
from ..utils import read_file
from .base import BaseSearchEngine


class Ascii2D(BaseSearchEngine):
    """API client for the Ascii2D image search engine.

    Ascii2D provides two search modes:
    1. Color search: Finds images with similar color combinations (default mode)
    2. Feature search: Finds images with similar visual features (bovw mode)

    Attributes:
        base_url: The base URL for Ascii2D searches.
        bovw: A flag to enable feature search mode.

    Note:
        - Color search (bovw=False) is recommended for finding visually similar images
        - Feature search (bovw=True) is better for:
            * Cropped images
            * Rotated images
            * Images with different color schemes
        - Feature search may be less accurate with heavily modified images
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

        This method supports two ways of searching:
        1. Search by image URL
        2. Search by uploading a local image file

        The search process involves:
        1. Initial submission of the image (URL or file)
        2. Optional switch to feature search mode if bovw=True
        3. Parsing and returning the search results

        Args:
            url: URL of the image to search.
            file: Local image file, can be a path string, bytes data, or Path object.
            **kwargs: Additional arguments passed to the parent class.

        Returns:
            Ascii2DResponse: An object containing:
                - Search results with similar images
                - Source information and metadata
                - The final search URL

        Raises:
            ValueError: If neither 'url' nor 'file' is provided.

        Note:
            - Only one of 'url' or 'file' should be provided
            - Feature search (bovw) may take longer to process
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