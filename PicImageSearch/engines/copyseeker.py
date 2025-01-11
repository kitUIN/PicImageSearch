from json import loads as json_loads
from json import dumps as json_dumps
import os
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

    def __init__(
        self, base_url: str = "https://copyseeker.net", **request_kwargs: Any
    ):
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

        data = {"discoveryType": "ReverseImageSearch"}

        if url:
            data["imageUrl"] = url
            headers = {
                    "next-action": "408936c3bdf458fbec6cf3c1253f56aefbcb4cf509",
                    "content-type": "text/plain;charset=UTF-8"
            }

            resp = await self._make_request(
                method="post",
                endpoint="",
                data=json_dumps([data]),
                headers=headers,
            )
        elif file:
            headers = {
                "next-action": "40dc303bfd320afd703a1a0a159464be4d64117f96",
                "content-type": "multipart/form-data; boundary=-"
            }
            files = {
                "1_file": (os.path.basename(file), read_file(file), "image/jpeg"),
                "1_discoveryType": (None, "ReverseImageSearch"),
                "0": (None, '["$K1"]')
            }
            files["1_discoveryType"] = (None, "ReverseImageSearch")
            files["0"] = (None, '["$K1"]')

            resp = await self._make_request(
                method="post",
                endpoint="",
                files=files,
                headers=headers
            )

            for line in resp.text.splitlines():
                line = line.strip()
                if line.startswith("1:{"):
                    return json_loads(line[2:]).get("discoveryId")
            return None


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
             "next-action": "4084b9ef4e0e6922ef12b23a4b8517be790fa67b88",
             "content-type": "text/plain;charset=UTF-8"
        }

        resp = await self._make_request(
            method="post", endpoint="discovery",data=json_dumps(data), headers=headers
        )
        
        for line in resp.text.splitlines():
            line = line.strip()
            if line.startswith("1:{"):
                resp_json = json_loads(line[2:])
        return CopyseekerResponse(resp_json, resp.url)
