from json import loads as json_loads
from pathlib import Path
from typing import Any, Optional, Union

from typing_extensions import override

from ..model import AnimeTraceResponse
from ..utils import read_file
from .base import BaseSearchEngine


class AnimeTrace(BaseSearchEngine[AnimeTraceResponse]):
    """API client for the AnimeTrace image search engine.

    Used for performing anime character recognition searches using AnimeTrace service.

    Attributes:
        base_url (str): The base URL for AnimeTrace API.
        is_multi (Optional[int]): Whether to show multiple results, 0 or 1.
        ai_detect (Optional[int]): Whether to enable AI image detection, 1 for yes, 2 for no.
    """

    def __init__(
        self,
        base_url: str = "https://api.animetrace.com",
        endpoint: str = "v1/search",
        is_multi: Optional[int] = None,
        ai_detect: Optional[int] = None,
        **request_kwargs: Any,
    ):
        """Initializes an AnimeTrace API client with specified configurations.

        Args:
            base_url (str): The base URL for AnimeTrace API, defaults to 'https://api.animetrace.com'.
            endpoint (str): The endpoint for AnimeTrace API, defaults to 'v1/search'.
            is_multi (Optional[int]): Whether to show multiple results, 0 or 1, defaults to None.
            ai_detect (Optional[int]): Whether to enable AI image detection, 1 for yes, 2 for no, defaults to None.
            **request_kwargs (Any): Additional arguments passed to the HTTP client.
        """
        base_url = f"{base_url}/{endpoint}"
        super().__init__(base_url, **request_kwargs)
        self.is_multi: Optional[int] = is_multi
        self.ai_detect: Optional[int] = ai_detect

    @override
    async def search(
        self,
        url: Optional[str] = None,
        file: Union[str, bytes, Path, None] = None,
        base64: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs: Any,
    ) -> AnimeTraceResponse:
        """Performs an anime character recognition search on AnimeTrace.

        This method supports three ways of searching:
            1. Search by image URL
            2. Search by uploading a local image file
            3. Search by providing a base64 encoded image

        Args:
            url (Optional[str]): URL of the image to search.
            file (Union[str, bytes, Path, None]): Local image file, can be a path string, bytes data, or Path object.
            base64 (Optional[str]): Base64 encoded image data.
            model (Optional[str]): Recognition model to use, defaults to None.
                Available models: 'anime_model_lovelive', 'pre_stable', 'anime', 'full_game_model_kira'.
            **kwargs (Any): Additional arguments passed to the request.

        Returns:
            AnimeTraceResponse: An object containing:
                - Detected characters with their source works
                - Bounding box coordinates
                - Additional metadata (trace_id, AI detection flag)

        Raises:
            ValueError: If none of `url`, `file`, or `base64` is provided.

        Note:
            - Only one of `url`, `file`, or `base64` should be provided.
            - URL and base64 searches use JSON POST requests.
            - File uploads use multipart/form-data POST requests.
        """
        params: dict[str, Any] = {}
        if self.is_multi:
            params["is_multi"] = self.is_multi
        if self.ai_detect:
            params["ai_detect"] = self.ai_detect
        if model:
            params["model"] = model

        if url:
            data = {"url": url, **params}
            resp = await self._send_request(
                method="post",
                json=data,
            )
        elif file:
            files = {"file": read_file(file)}
            resp = await self._send_request(
                method="post",
                files=files,
                data=params or None,
            )
        elif base64:
            data = {"base64": base64, **params}
            resp = await self._send_request(
                method="post",
                json=data,
            )
        else:
            raise ValueError("One of 'url', 'file', or 'base64' must be provided")

        return AnimeTraceResponse(json_loads(resp.text), resp.url)
