import re
from base64 import b64encode
from json import dumps as json_dumps
from json import loads as json_loads
from pathlib import Path
from typing import Any, Optional, Union

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

    async def _upload_image(self, file: Union[str, bytes, Path]) -> tuple[str, str]:
        """Uploads an image to Bing and retrieves the BCID.

        Args:
            file: Local image file (path or bytes) to search.

        Returns:
            str: The BCID (Bing Correlation ID) associated with the uploaded image.

        Raises:
            ValueError: If the BCID cannot be found on the page after upload.
        """
        url = f"{self.base_url}/images/search?view=detailv2&iss=sbiupload"
        image_base64 = b64encode(read_file(file)).decode("utf-8")
        files = {
            "cbir": "sbi",
            "imageBin": image_base64,
        }
        response = await self.post(url, files=files)

        if match := re.search(r"(bcid_[A-Za-z0-9-.]+)", response.text):
            return match[1], str(response.url)
        else:
            raise ValueError("BCID not found on page.")

    async def _get_insights(
        self, bcid: Optional[str] = None, image_url: Optional[str] = None
    ) -> dict:
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
        insights_url = (
            f"{self.base_url}/images/api/custom/knowledge"
            "?rshighlight=true&textDecorations=true&internalFeatures=share"
            "&nbl=1&FORM=SBIHMP&safeSearch=off&mkt=en-us&setLang=en-us&IID=idpins&SFX=1"
        )

        if image_url:
            insights_headers = {
                "Referer": (
                    f"{self.base_url}/images/search?"
                    f"view=detailv2&iss=sbi&FORM=SBIHMP&sbisrc=UrlPaste"
                    f"&q=imgurl:{image_url}&idpbck=1"
                )
            }
            files = {
                "knowledgeRequest": (
                    None,
                    json_dumps({"imageInfo": {"url": image_url, "source": "Url"}}),
                )
            }
            response = await self.post(
                insights_url, headers=insights_headers, files=files
            )

        elif bcid:
            insights_url += f"&insightsToken={bcid}"
            insights_headers = {
                "Referer": f"{self.base_url}/images/search?insightsToken={bcid}",
            }
            data = {"imageInfo": {"imageInsightsToken": bcid}, "knowledgeRequest": {}}
            self.client.cookies = None
            response = await self.post(
                insights_url, headers=insights_headers, data=data
            )
        else:
            raise ValueError("Either bcid or image_url must be provided")

        return json_loads(response.text)

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

        if url:
            resp_url = (
                f"{self.base_url}/images/search?"
                f"view=detailv2&iss=sbi&FORM=SBIHMP&sbisrc=UrlPaste"
                f"&q=imgurl:{url}&idpbck=1"
            )
            json_response = await self._get_insights(image_url=url)

        else:
            bcid, resp_url = await self._upload_image(file)
            json_response = await self._get_insights(bcid=bcid)

        return BingResponse(json_response, resp_url)
