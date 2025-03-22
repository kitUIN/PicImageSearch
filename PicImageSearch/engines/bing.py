import re
from base64 import b64encode
from json import dumps as json_dumps
from json import loads as json_loads
from pathlib import Path
from typing import Any, Optional, Union
from urllib.parse import quote_plus

from typing_extensions import override

from ..model import BingResponse
from ..utils import read_file
from .base import BaseSearchEngine


class Bing(BaseSearchEngine[BingResponse]):
    """API client for the Bing image search engine.

    Used for performing reverse image searches using Bing's API.

    Attributes:
        base_url (str): The base URL for Bing searches.
    """

    def __init__(self, **request_kwargs: Any):
        """Initializes a Bing API client with specified configurations.

        Args:
            **request_kwargs (Any): Additional arguments for network requests.
        """
        base_url = "https://www.bing.com"
        super().__init__(base_url, **request_kwargs)

    async def _upload_image(self, file: Union[str, bytes, Path]) -> tuple[str, str]:
        """Uploads an image to Bing and retrieves the BCID.

        Args:
            file (Union[str, bytes, Path]): Local image file, can be a path string, bytes data, or Path object.

        Returns:
            tuple[str, str]: A tuple containing:
                - The BCID (Bing Correlation ID) associated with the uploaded image
                - The response URL from Bing's search page

        Raises:
            ValueError: If the BCID cannot be found in the response page.
        """
        endpoint = "images/search?view=detailv2&iss=sbiupload"
        image_base64 = b64encode(read_file(file)).decode("utf-8")
        files = {
            "cbir": "sbi",
            "imageBin": image_base64,
        }
        resp = await self._send_request(method="post", endpoint=endpoint, files=files)

        if match := re.search(r"(bcid_[A-Za-z0-9-.]+)", resp.text):
            return match[1], str(resp.url)

        raise ValueError("BCID not found on page.")

    async def _get_insights(self, bcid: Optional[str] = None, image_url: Optional[str] = None) -> dict[str, Any]:
        """Retrieves image insights from Bing using either BCID or image URL.

        This method handles two search scenarios:
            1. Search by image URL directly
            2. Search by BCID (obtained after uploading an image)

        Args:
            bcid (Optional[str]): The BCID (Bing Correlation ID) retrieved after uploading an image.
            image_url (Optional[str]): The URL of the image to search for.

        Returns:
            dict: The JSON response containing insights about the image.

        Raises:
            ValueError: If neither bcid nor image_url is provided.
        """
        endpoint = "images/api/custom/knowledge"

        params: dict[str, Any] = {
            "rshighlight": "true",
            "textDecorations": "true",
            "internalFeatures": "similarproducts,share",
            "nbl": "1",
            "FORM": "SBIHMP",
            "safeSearch": "off",
            "mkt": "en-us",
            "setLang": "en-us",
            "iss": "sbi",
            "IID": "idpins",
            "SFX": "1",
        }

        if image_url:
            referer = (
                f"{self.base_url}/images/search?"
                f"view=detailv2&iss=sbi&FORM=SBIHMP&sbisrc=UrlPaste"
                f"&q=imgurl:{quote_plus(image_url)}&idpbck=1"
            )
            image_info = {"imageInfo": {"url": image_url, "source": "Url"}}

        else:
            params["insightsToken"] = bcid
            referer = f"{self.base_url}/images/search?insightsToken={bcid}"
            image_info = {"imageInfo": {"imageInsightsToken": bcid, "source": "Gallery"}}

            if self.client:
                self.client.cookies.clear()

        headers = {"Referer": referer}
        files = {
            "knowledgeRequest": (
                None,
                json_dumps(image_info),
                "application/json",
            )
        }
        resp = await self._send_request(method="post", endpoint=endpoint, headers=headers, params=params, files=files)

        return json_loads(resp.text)

    @override
    async def search(
        self,
        url: Optional[str] = None,
        file: Union[str, bytes, Path, None] = None,
        **kwargs: Any,
    ) -> BingResponse:
        """Performs a reverse image search on Bing.

        This method supports two ways of searching:
            1. Search by image URL
            2. Search by uploading a local image file

        Args:
            url (Optional[str]): URL of the image to search.
            file (Union[str, bytes, Path, None]): Local image file, can be a path string, bytes data, or Path object.
            **kwargs (Any): Additional arguments passed to the parent class.

        Returns:
            BingResponse: An object containing the search results and metadata.

        Raises:
            ValueError: If neither `url` nor `file` is provided.
            ValueError: If BCID cannot be found when uploading an image.

        Note:
            - Only one of `url` or `file` should be provided.
            - The search process involves multiple HTTP requests to Bing's API.
        """
        if url:
            resp_url = (
                f"{self.base_url}/images/search?"
                f"view=detailv2&iss=sbi&FORM=SBIHMP&sbisrc=UrlPaste"
                f"&q=imgurl:{url}&idpbck=1"
            )
            resp_json = await self._get_insights(image_url=url)

        elif file:
            bcid, resp_url = await self._upload_image(file)
            resp_json = await self._get_insights(bcid=bcid)
        else:
            raise ValueError("Either 'url' or 'file' must be provided")

        return BingResponse(resp_json, resp_url)
