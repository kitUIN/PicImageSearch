from json import loads as json_loads
from pathlib import Path
from typing import Any, Optional, Union

from ..model import CopyseekerResponse
from ..utils import read_file
from .base import BaseSearchEngine


class Copyseeker(BaseSearchEngine):
    """API client for the Copyseeker image search engine.

    Used for performing reverse image searches using Copyseeker service.

    Attributes:
        base_url: The base URL for Copyseeker searches.
    """

    def __init__(
        self, base_url: str = "https://api.copyseeker.net", **request_kwargs: Any
    ):
        """Initializes a Copyseeker API client.

        Args:
            base_url: The base URL for Copyseeker searches.
            **request_kwargs: Additional arguments for network requests.
        """
        super().__init__(base_url, **request_kwargs)

    async def _get_discovery_id(
        self, url: Optional[str] = None, file: Union[str, bytes, Path, None] = None
    ):

        data = {"discoveryType": "ReverseImageSearch"}

        if url:
            data["imageUrl"] = url
            resp = await self._make_request(
                method="post",
                endpoint="OnTriggerDiscoveryByUrl",
                json=data,
            )
        elif file:
            files = {"file": read_file(file)}
            resp = await self._make_request(
                method="post",
                endpoint="OnTriggerDiscoveryByFile",
                data=data,
                files=files,
            )

        resp_json = json_loads(resp.text)  # noqa
        return resp_json.get("discoveryId")

    async def search(
        self,
        url: Optional[str] = None,
        file: Union[str, bytes, Path, None] = None,
        **kwargs: Any,
    ) -> CopyseekerResponse:
        """Performs a reverse image search on Copyseeker.

        Supports searching by image URL or by uploading an image file.

        Requires either 'url' or 'file' to be provided.

        Args:
            url: URL of the image to search.
            file: Local image file (path or bytes) to search.

        Returns:
            CopyseekerResponse: Contains search results and additional information.

        Raises:
            ValueError: If neither 'url' nor 'file' is provided.

        Note:
            The search process involves multiple HTTP requests to Copyseeker's API.
        """
        await super().search(url, file, **kwargs)

        discovery_id = await self._get_discovery_id(url, file)
        if discovery_id is None:
            return CopyseekerResponse({}, "")

        data = {"discoveryId": discovery_id, "hasBlocker": False}

        resp = await self._make_request(
            method="post", endpoint="OnProvideDiscovery", json=data
        )
        resp_json = json_loads(resp.text)
        return CopyseekerResponse(resp_json, resp.url)
