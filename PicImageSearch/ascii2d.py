from pathlib import Path
from typing import Any, Dict, Optional, Union

from .model import Ascii2DResponse
from .network import HandOver


class Ascii2D(HandOver):
    """
    Ascii2D

    Reverse image from https://ascii2d.net

    Note:
        Use color combination search instead if the image has nearly the same aspect ration and is very similar in their
        entirety to the original.
        Use feature search instead for images with partially matchint features, such as cropped images or rotated
        images. If there is not even half of the image in the original left you won't have much luck with this option
        either.

    Args:
        bovw: Use feature search instead of color combination search, default False
        **request_kwargs: Additional keyword arguments to configure the network request.
            This may include proxy settings and other request-specific options. See `.network.HandOver` for details.

    Attributes:
        bovw: Use feature search instead of color combination search, default False
    """

    def __init__(self, bovw: bool = False, **request_kwargs: Any):
        super().__init__(**request_kwargs)
        self.bovw: bool = bovw

    async def search(
        self, url: Optional[str] = None, file: Union[str, bytes, Path, None] = None
    ) -> Ascii2DResponse:
        """
        Ascii2D Search

        Perform a reverse image search on https://ascii2d.net using the URL or file of the image.
        The user must provide either a URL or a file.

        Args:
            url: URL of the image to search.
            file: Image file to search. Can be a file path (str or Path) or raw bytes.

        Returns:
            An instance of Ascii2DResponse containing the search results and additional metadata.

        Raises:
            ValueError: If neither `url` nor `file` is provided.

        Note:
            The returned `Ascii2DResponse` object contains the following attributes:
            - `.origin`: The raw data obtained from the scraper.
            - `.raw`: A simplified version of the scraped data.
            - `.raw[0]`: The first result in the simplified data set.
            - `.raw[0].title`: The title of the first result.
            - `.raw[0].url`: The source URL of the first result.
            - `.raw[0].authors`: The authors of the first result.
            - `.raw[0].thumbnail`: The thumbnail image URL of the first result.
            - `.raw[0].detail`: The detail page URL of the first result.
        """
        if url:
            ascii2d_url = "https://ascii2d.net/search/uri"
            resp = await self.post(ascii2d_url, data={"uri": url})
        elif file:
            ascii2d_url = "https://ascii2d.net/search/file"
            files: Dict[str, Any] = {
                "file": file if isinstance(file, bytes) else open(file, "rb")
            }
            resp = await self.post(ascii2d_url, files=files)
        else:
            raise ValueError("url or file is required")

        # 如果启用bovw选项，第一次请求是向服务器提交文件
        # If the bovw option is enabled, the first request is only used to submit the file to the server
        if self.bovw:
            resp = await self.get(resp.url.replace("/color/", "/bovw/"))

        return Ascii2DResponse(resp.text, resp.url)
