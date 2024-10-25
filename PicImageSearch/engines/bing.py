import base64
import re
from pathlib import Path
from typing import Any, Optional, Union

import httpx

from ..model import BingResponse
from ..utils import read_file
from .base import BaseSearchEngine


class Bing(BaseSearchEngine):
    """API client for the Bing image search engine.

    Used for performing reverse image searches using Bing's API.

    Attributes:
        base_url: The base URL for Bing searches.
    """

    def __init__(self, base_url: str = "https://www.bing.com", **request_kwargs: Any):
        """Initializes a Bing API client with specified configurations.

        Args:
            base_url: The base URL for Bing searches.
            **request_kwargs: Additional arguments for network requests.
        """
        super().__init__(base_url, **request_kwargs)

    async def _upload_image(self, file: Union[str, bytes, Path]) -> str:
        """Uploads an image to Bing and retrieves the BCID.

        Args:
            file: Local image file (path or bytes) to search.

        Returns:
            str: The BCID (Bing Correlation ID) associated with the uploaded image.

        Raises:
            ValueError: If the BCID cannot be found on the page after upload.
        """
        url = f"{self.base_url}/images/search?view=detailv2&iss=sbiupload"
        image_base64 = base64.b64encode(read_file(file)).decode("utf-8")
        files = {
            "imgurl": (None, ""),
            "cbir": (None, "sbi"),
            "imageBin": (None, image_base64),
        }
        async with httpx.AsyncClient(http2=True, follow_redirects=True) as client:
            response = await client.post(url, files=files)
            response.raise_for_status()

        match = re.search(r"(bcid_[A-Za-z0-9-.]+)", response.text)
        if match:
            return match.group(1)
        else:
            raise ValueError("BCID not found on page.")

    async def _get_insights(self, bcid: str, image_url: Optional[str] = None) -> dict:
        """Retrieves insights from Bing using the BCID or image URL.

        Args:
            bcid: The BCID (Bing Correlation ID) retrieved after uploading an image.
            image_url: The URL of the image to search for.

        Returns:
            dict: The JSON response containing insights about the image.

        Raises:
            ValueError: If neither `bcid` nor `image_url` is provided.
            httpx.HTTPStatusError: If the HTTP request to Bing fails.
        """
        insights_url = f"{self.base_url}/images/api/custom/knowledge?rshighlight=true&textDecorations=true&internalFeatures=share&nbl=1&FORM=SBIHMP&safeSearch=off&mkt=en-us&setLang=en-us&IID=idpins&SFX=1"

        if image_url:
            ref = f"{self.base_url}/images/search?view=detailv2&iss=sbi&FORM=SBIHMP&sbisrc=UrlPaste&q=imgurl:{image_url}&idpbck=1"
            insights_headers = {
                "Referer": ref,
                "Content-Type": "multipart/form-data; boundary=boundary",
            }
            body = (
                "--boundary\r\n"
                'Content-Disposition: form-data; name="knowledgeRequest"\r\n\r\n'
                '{"imageInfo": {"url": "' + image_url + '"}}\r\n'
                "--boundary--"
            )

        elif bcid:
            insights_url += f"&insightsToken={bcid}"
            insights_headers = {
                "Referer": f"{self.base_url}/images/search?insightsToken={bcid}",
                "Content-Type": "multipart/form-data; boundary=boundary",
            }
            body = (
                "--boundary\r\n"
                'Content-Disposition: form-data; name="knowledgeRequest"\r\n\r\n'
                '{"imageInfo": {"imageInsightsToken": "' + bcid + '"}, "knowledgeRequest": {}}\r\n'
                "--boundary--"
            )
        else:
            raise ValueError("Either bcid or image_url must be provided")

        async with httpx.AsyncClient(http2=True) as client:
            response = await client.post(insights_url, headers=insights_headers, data=body.encode('utf-8'))
            response.raise_for_status()
            return response.json()

    async def search(
        self,
        url: Optional[str] = None,
        file: Union[str, bytes, Path, None] = None,
        **kwargs: Any,
    ) -> BingResponse:
        """Performs a reverse image search on Bing.

        Supports searching by image URL or by uploading an image file.

        Requires either 'url' or 'file' to be provided.

        Args:
            url: URL of the image to search.
            file: Local image file (path or bytes) to search.

        Returns:
            BingResponse: Contains search results and additional information.

        Raises:
            ValueError: If neither 'url' nor 'file' is provided.
        
        Note:
            The search process involves multiple HTTP requests to Bing's API.
        """
        await super().search(url, file, **kwargs)
        insights_url = "" 

        if url:
            insights_url = f"{self.base_url}/images/api/custom/knowledge?rshighlight=true&textDecorations=true&internalFeatures=share&nbl=1&FORM=SBIHMP&safeSearch=off&mkt=en-us&setLang=en-us&IID=idpins&SFX=1"
            json_response = await self._get_insights(bcid=None, image_url=url)

        elif file:
            bcid = await self._upload_image(file)
            insights_url = f"{self.base_url}/images/api/custom/knowledge?rshighlight=true&textDecorations=true&internalFeatures=share&nbl=1&FORM=SBIHMP&safeSearch=off&mkt=en-us&setLang=en-us&IID=idpins&SFX=1&insightsToken={bcid}"

            json_response = await self._get_insights(bcid=bcid)
        else:
            raise ValueError("Either url or file must be provided")

        return BingResponse(json_response, insights_url)