from pathlib import Path
from typing import Any, Optional, Union

import os
from json import loads as json_loads

from ..model import CopyseekerItem, CopyseekerResponse
from ..utils import read_file
from .base import BaseSearchEngine

class Copyseeker(BaseSearchEngine):
    """API client for the Copyseeker image search engine.

    Used for performing reverse image searches using Copyseeker service.

    Attributes:
        base_url: The base URL for Copyseeker searches.
    """

    def __init__(
        self,
        base_url: str = "https://api.copyseeker.net",
        **request_kwargs: Any
    ):
        """Initializes a Copyseeker API client.

        Args:
            base_url: The base URL for Copyseeker searches.
            **request_kwargs: Additional arguments for network requests.
        """
        super().__init__(base_url, **request_kwargs)


    async def _get_discovery_id(
        self,
        url: Optional[str] = None,
        file: Union[str, bytes, Path, None] = None
    ):

        if url:
            payload = {
                "imageUrl": url,
                "discoveryType": "ReverseImageSearch"
            }
            resp = await self._make_request(method="post", endpoint="OnTriggerDiscoveryByUrl", json=payload)
        elif file:
            files = {"file": read_file(file)}
            resp = await self._make_request(
                method="post",
                endpoint="OnTriggerDiscoveryByFile",
                files=files,
                data={"discoveryType": "ReverseImageSearch"}
            )
        else:
            raise ValueError("Either 'url' or 'file' must be provided")

        json_response = json_loads(resp.text)
        return json_response.get("discoveryId")
        


    async def search(
        self,
        url: Optional[str] = None,
        file: Union[str, bytes, Path, None] = None, **kwargs: Any
    ) -> CopyseekerResponse:
        
        await super().search(url, file, **kwargs)

        discovery_id = await self._get_discovery_id(url, file)
        if discovery_id is None:
            return CopyseekerResponse({}, "")

        data = {
            "discoveryId": discovery_id,
            "hasBlocker": False
        }

        resp = await self._make_request(method="post", endpoint="OnProvideDiscovery", json=data)
        resp_json = json_loads(resp.text)
        return CopyseekerResponse(resp_json, resp.url)