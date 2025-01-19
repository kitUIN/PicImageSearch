import os
from json import dumps as json_dumps
from json import loads as json_loads
from pathlib import Path
from typing import Any, Optional, Union

from ..model import CopyseekerResponse
from ..utils import read_file
from .base import BaseSearchEngine


class Copyseeker(BaseSearchEngine[CopyseekerResponse]):
    """API client for the Copyseeker image search engine.

    Used for performing reverse image searches using Copyseeker service.

    Attributes:
        base_url (str): The base URL for Copyseeker searches.
    """

    def __init__(self, base_url: str = "https://copyseeker.net", **request_kwargs: Any):
        """Initializes a Copyseeker API client.

        Args:
            base_url (str): The base URL for Copyseeker searches.
            **request_kwargs (Any): Additional arguments for network requests.
        """
        super().__init__(base_url, **request_kwargs)

    async def _get_discovery_id(
        self, url: Optional[str] = None, file: Union[str, bytes, Path, None] = None
    ) -> Optional[str]:
        """Retrieves a discovery ID from Copyseeker for image search.

        This method handles two search scenarios:
            1. Search by image URL
            2. Search by uploading a local image file

        Args:
            url (Optional[str]): URL of the image to search.
            file (Union[str, bytes, Path, None]): Local image file, can be a path string, bytes data, or Path object.

        Returns:
            Optional[str]: The discovery ID if successful, None otherwise.

        Note:
            - The discovery ID is required for retrieving search results.
        """

        resp = None
        discovery_id = None

        if url:
            data = {"discoveryType": "ReverseImageSearch", "imageUrl": url}
            headers = {
                "next-action": "4004c826c84c7592d782ef3648ac6da33ae40f0893",
                "content-type": "text/plain;charset=UTF-8",
            }

            resp = await self._make_request(
                method="post",
                headers=headers,
                data=json_dumps([data]),
            )
        elif file:
            files = {
                "1_file": (os.path.basename(file), read_file(file), "image/jpeg"),
                "1_discoveryType": (None, "ReverseImageSearch"),
                "0": (None, '["$K1"]'),
            }
            headers = {
                "next-action": "40da2b6c4059b8a099c6634d796264254d3c0e12ab",
                "content-type": "multipart/form-data; boundary=-",
            }

            resp = await self._make_request(
                method="post",
                headers=headers,
                files=files,
            )

        if resp:
            for line in resp.text.splitlines():
                line = line.strip()
                if line.startswith("1:{"):
                    discovery_id = json_loads(line[2:]).get("discoveryId")
                    break

        return discovery_id

    async def search(
        self,
        url: Optional[str] = None,
        file: Union[str, bytes, Path, None] = None,
        **kwargs: Any,
    ) -> CopyseekerResponse:
        """Performs a reverse image search on Copyseeker.

        This method supports two ways of searching:
            1. Search by image URL
            2. Search by uploading a local image file

        The search process involves two steps:
            1. Obtaining a discovery ID
            2. Retrieving search results using the discovery ID

        Args:
            url (Optional[str]): URL of the image to search.
            file (Union[str, bytes, Path, None]): Local image file, can be a path string, bytes data, or Path object.
            **kwargs (Any): Additional arguments passed to the parent class.

        Returns:
            CopyseekerResponse: An object containing search results and metadata.
                Returns an empty response if discovery ID cannot be obtained.

        Raises:
            ValueError: If neither `url` nor `file` is provided.

        Note:
            - Only one of `url` or `file` should be provided.
            - The search process involves multiple HTTP requests to Copyseeker's API.
        """
        self._validate_args(url, file)

        discovery_id = await self._get_discovery_id(url, file)
        if discovery_id is None:
            return CopyseekerResponse({}, "")

        data = [{"discoveryId": discovery_id, "hasBlocker": "False"}]
        headers = {
            "next-action": "4051bb75bb1a1a40d49e0cf17d929f2a113217b6f3",
            "content-type": "text/plain;charset=UTF-8",
        }

        resp = await self._make_request(
            method="post", endpoint="discovery", data=json_dumps(data), headers=headers
        )

        resp_json = {}

        for line in resp.text.splitlines():
            line = line.strip()
            if line.startswith("1:{"):
                resp_json = json_loads(line[2:])
                break

        return CopyseekerResponse(resp_json, resp.url)
