import re
from base64 import b64decode, b64encode
from json import dumps as json_dumps
from json import loads as json_loads
from pathlib import Path
from typing import Any
from urllib.parse import quote_plus

from typing_extensions import override

from ..model import BingResponse
from ..utils import read_file
from .base import BaseSearchEngine


def _decrypt_signature_segment(encrypted_segment: str) -> str:
    """Decrypts an encrypted signature segment using XOR cipher with offset.

    The decryption process:
    1. Base64 decode the encrypted segment
    2. XOR each byte with corresponding key character
    3. Subtract offset to get final character

    Args:
        encrypted_segment: Base64-encoded encrypted signature segment.

    Returns:
        Decrypted signature segment, or original value if decryption fails.
    """
    # Bing's signature encryption key and offset
    ENCRYPTION_KEY = "AAAAC3NzaC1lZDI1NTE5AAAAIGd3gMN2v1KRLBGmotz7jbQYF8PaB+Jpe6iVf2YIeN5b"
    CHAR_OFFSET = 3

    try:
        decoded_bytes = b64decode(encrypted_segment)
    except Exception:
        return encrypted_segment

    decrypted_chars = []
    for i, cipher_byte in enumerate(decoded_bytes):
        key_char_code = ord(ENCRYPTION_KEY[i % len(ENCRYPTION_KEY)])
        xor_result = cipher_byte ^ key_char_code
        original_char_code = xor_result - CHAR_OFFSET
        decrypted_chars.append(chr(original_char_code))

    return "".join(decrypted_chars)


def _parse_signature(raw_signature: str) -> str:
    """Parses and decrypts a raw signature string.

    Expected format: "version|encrypted_data|timestamp"

    Args:
        raw_signature: Raw signature string from Bing response.

    Returns:
        Decrypted signature in format "version|decrypted_data|timestamp",
        or original signature if format is invalid.
    """
    parts = raw_signature.split("|")
    if len(parts) == 3:
        version, encrypted_data, timestamp = parts
        decrypted_data = _decrypt_signature_segment(encrypted_data)
        return f"{version}|{decrypted_data}|{timestamp}"
    return raw_signature


class Bing(BaseSearchEngine[BingResponse]):
    """API client for the Bing image search engine.

    Used for performing reverse image searches using Bing's API.

    Attributes:
        base_url (str): The base URL for Bing searches.
        _session_key (str | None): Session key obtained from Bing during search operations.
        _image_signature (str | None): Image signature used for authentication headers.
    """

    def __init__(self, **request_kwargs: Any):
        """Initializes a Bing API client with specified configurations.

        Args:
            **request_kwargs (Any): Additional arguments for network requests.
        """
        base_url = "https://www.bing.com"
        super().__init__(base_url, **request_kwargs)
        self._session_key: str | None = None
        self._image_signature: str | None = None

    async def _upload_image(self, file: str | bytes | Path) -> tuple[str, str]:
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

        # Extract session key and image signature from response
        self._session_key = re.search(r"skey=([^&]+)", resp.text)[1]
        self._image_signature = re.search(r"imageSignature&quot;:&quot;(.+?)&quot;", resp.text)[1]

        # Extract BCID from response
        if match := re.search(r"(bcid_[A-Za-z0-9-.]+)", resp.text):
            return match[1], str(resp.url)

        raise ValueError("BCID not found on page.")

    async def _get_insights(self, bcid: str | None = None, image_url: str | None = None) -> dict[str, Any]:
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

        # Base parameters for the insights request
        params: dict[str, Any] = {
            "rshighlight": "true",
            "textDecorations": "true",
            "internalFeatures": "similarproducts,share",
            "nbl": "1",
            "skey": self._session_key,
            "safeSearch": "off",
            "mkt": "en-us",
            "setLang": "en-us",
            "iss": "SBIUPLOADGET",
            "IID": "idpins",
            "SFX": "1",
        }

        # Configure request based on search mode
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

            # Clear cookies for BCID-based search
            if self.client:
                self.client.cookies.clear()

        # Build headers with signature if available
        headers = {"Referer": referer}
        if self._image_signature:
            headers["X-Image-Knowledge-Signature"] = _parse_signature(self._image_signature)

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
        url: str | None = None,
        file: str | bytes | Path | None = None,
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
            # Build search URL and extract signature
            resp_url = (
                f"{self.base_url}/images/search?"
                f"view=detailv2&iss=sbi&FORM=SBIHMP&sbisrc=UrlPaste"
                f"&q=imgurl:{url}&idpbck=1"
            )
            resp_text, _, _ = await self.get(resp_url)
            self._image_signature = re.search(r"imageSignature&quot;:&quot;(.+?)&quot;", resp_text)[1]
            resp_json = await self._get_insights(image_url=url)

        elif file:
            # Upload image and get insights using BCID
            bcid, resp_url = await self._upload_image(file)
            resp_json = await self._get_insights(bcid=bcid)
        else:
            raise ValueError("Either 'url' or 'file' must be provided")

        return BingResponse(resp_json, resp_url)
