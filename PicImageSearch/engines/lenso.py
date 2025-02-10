import base64
from json import loads as json_loads

from pathlib import Path
from typing import Any, Optional, Union

from ..model import LensoResponse
from ..utils import read_file
from .base import BaseSearchEngine


class Lenso(BaseSearchEngine[LensoResponse]):
    """API client for the Lenso image search engine.

    Lenso is a powerful AI-driven visual search engine that helps you find similar images,
    duplicates, recognize places, and discover related content.

    Attributes:
        base_url (str): The base URL for Lenso API.

    Supported search types (type parameter):
        (default) It can be empty and then it will give all possible types, but in smaller quantities
        - `similar`: Find visually similar images.
        - `duplicates`: Find duplicate images.
        - `places`:  Recognize places in the image.
        - `related`: Find related images.

    Supported sort options (sort parameter):
        - `SMART` (default): Lenso's default smart sorting.
        - `RANDOM`: Randomly sorted results.
        - `QUALITY_DESCENDING`: Sort by quality, best to worst match.
        - `QUALITY_ASCENDING`: Sort by quality, worst to best match.
        - `DATE_DESCENDING`: Sort by date, newest to oldest.
        - `DATE_ASCENDING`: Sort by date, oldest to newest.
    """

    def __init__(
        self,
        base_url: str = "https://lenso.ai",
        **request_kwargs: Any,
    ):
        """Initializes a Lenso API client with request configuration.

        Args:
            base_url (str): The base URL for Lenso API.
            **request_kwargs (Any): Additional arguments for network requests.
        """
        super().__init__(base_url, **request_kwargs)
        self.base_url = base_url.rstrip('/')

    async def _upload_image(self, image_base64: str) -> str:
        """Uploads an image to Lenso API and retrieves the result hash.

        Args:
            image_base64 (str): Base64 encoded image data.

        Returns:
            str: The ID (hash) of the uploaded image.

        Raises:
            RuntimeError: If the upload fails or ID is not found in response.
        """
        endpoint = "api/upload"
        payload = {"image": f"data:image/jpeg;base64,{image_base64}"}
        resp = await self._make_request(
            method="post",
            endpoint=endpoint,
            json=payload
        )
        resp_json = json_loads(resp.text)
        result_hash = resp_json.get('id')
        if not result_hash:
            raise RuntimeError(f"Lenso Upload failed or ID not found. Status Code: {resp.status_code}, Response: {resp.text}")
        return result_hash


    async def search(
        self,
        url: Optional[str] = None,
        file: Union[str, bytes, Path, None] = None,
        search_type: str = "",
        sort_type: str = "SMART",
        **kwargs: Any,
    ) -> LensoResponse:
        """Performs a reverse image search on Lenso.

        This method supports two ways of searching:
            1. Search by image URL
            2. Search by uploading a local image file

        Args:
            url (Optional[str]): URL of the image to search.
            file (Union[str, bytes, Path, None]): Local image file, can be a path string, bytes data, or Path object.
            search_type (str): Type of search to perform. Options are 'similar', 'duplicates', 'places', 'related'. Defaults to 'similar'.
            sort_type (str): Sorting method for results. Options are 'SMART', 'RANDOM', 'QUALITY_DESCENDING', 'QUALITY_ASCENDING', 'DATE_DESCENDING', 'DATE_ASCENDING'. Defaults to 'SMART'.
            **kwargs (Any): Additional arguments passed to the parent class.

        Returns:
            LensoResponse: An object containing:
                - Search results from Lenso API
                - Metadata about the search

        Raises:
            ValueError: If neither `url` nor `file` is provided.
            RuntimeError: If image upload to Lenso fails.
        """
        self._validate_args(url, file)

        image_base64: str = ""
        result_hash: str = ""

        if url:
            image_bytes = await self.download(url)
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            result_hash = await self._upload_image(image_base64)

        elif file:
            image_bytes = read_file(file)
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            result_hash = await self._upload_image(image_base64)
        else:
            raise ValueError("Either 'url' or 'file' must be provided for Lenso search.")


        search_endpoint = "api/search"
        search_payload = {
            "image": {
                "id": result_hash,
                "data": f"data:image/jpeg;base64,{image_base64}"
            },
            "effects": {},
            "selection": {},
            "domain": "",
            "text": "",
            "page": 0,
            "type": search_type,
            "sort": sort_type,
            "seed": 0,
            "facial_search_consent": 0
        }


        resp = await self._make_request(
            method="post",
            endpoint=search_endpoint,
            json=search_payload
        )

        return LensoResponse(json_loads(resp.text), resp.url)
