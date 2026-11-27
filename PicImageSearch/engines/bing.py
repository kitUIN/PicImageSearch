import re
from base64 import b64decode, b64encode
from json import dumps as json_dumps
from json import loads as json_loads
from pathlib import Path
from typing import Any

from typing_extensions import override

from ..model import BingResponse
from ..network import RESP
from ..utils import read_file
from .base import BaseSearchEngine


def _decrypt_signature_segment(encrypted_segment: str, key: str, offset: int) -> str:
    """Decrypts an encrypted signature segment using XOR cipher with offset.

    The decryption process:
    1. Base64 decode the encrypted segment
    2. XOR each byte with corresponding key character
    3. Subtract offset to get final character

    Args:
        encrypted_segment: Base64-encoded encrypted signature segment.
        key: Encryption key provided by the Bing search page.
        offset: Character offset provided by the Bing search page.

    Returns:
        Decrypted signature segment, or original value if decryption fails.
    """
    try:
        decoded_bytes = b64decode(encrypted_segment)
    except Exception:
        return encrypted_segment

    decrypted_chars = []
    for i, cipher_byte in enumerate(decoded_bytes):
        key_char_code = ord(key[i % len(key)])
        xor_result = cipher_byte ^ key_char_code
        original_char_code = xor_result - offset
        decrypted_chars.append(chr(original_char_code))

    return "".join(decrypted_chars)


def _parse_signature(raw_signature: str, key: str, offset: int) -> str:
    """Parses and decrypts a raw signature string.

    Expected format: "version|encrypted_data|timestamp"

    Args:
        raw_signature: Raw signature string from Bing response.
        key: Encryption key provided by the Bing search page.
        offset: Character offset provided by the Bing search page.

    Returns:
        Decrypted signature in format "v2u|decrypted_data|timestamp",
        or original signature if format is invalid.
    """
    parts = raw_signature.split("|")
    if len(parts) == 3:
        _, encrypted_data, timestamp = parts
        decrypted_data = _decrypt_signature_segment(encrypted_data, key, offset)
        return f"v2u|{decrypted_data}|{timestamp}"
    return raw_signature


class Bing(BaseSearchEngine[BingResponse]):
    """API client for the Bing image search engine.

    Used for performing reverse image searches using Bing's API.

    Note:
        Bing keeps the search session in cookies, so pass a shared `client` to keep them between requests.

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
            ValueError: If the BCID or the image signature cannot be found in the response page.
        """
        endpoint = "images/search?view=detailv2&iss=sbiupload"
        image_base64 = b64encode(read_file(file)).decode("utf-8")
        files = {
            "cbir": "sbi",
            "imageBin": image_base64,
        }
        resp = await self._send_request(method="post", endpoint=endpoint, files=files)
        return self._parse_search_page(resp), str(resp.url)

    def _parse_search_page(self, resp: RESP) -> str:
        """Extracts the session key and image signature from a search page and returns the BCID.

        Args:
            resp (RESP): The search page Bing redirects to after an image is submitted.

        Returns:
            str: The BCID (Bing Correlation ID) associated with the image.

        Raises:
            ValueError: If the BCID or the image signature cannot be found in the response page.
        """
        session_key = re.search(r"skey=([^&]+)", resp.text)
        signature = re.search(r'data-image-signature="([^"]+)"', resp.text)
        signature_init = re.search(r'SignatureUtils\.init\("([^"]+)",\s*(\d+)\)', resp.text)
        bcid = re.search(r"bcid=([^&]+)", resp.url)
        if not (session_key and signature and signature_init and bcid):
            raise ValueError("BCID or image signature not found on page.")

        self._session_key = session_key[1]
        self._image_signature = _parse_signature(signature[1], signature_init[1], int(signature_init[2]))
        return f"bcid_{bcid[1]}"

    async def _get_insights(self, bcid: str) -> dict[str, Any]:
        """Retrieves image insights from Bing using BCID.

        Args:
            bcid (str): The BCID (Bing Correlation ID) retrieved from the search page.

        Returns:
            dict: The JSON response containing insights about the image.
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
            "insightsToken": bcid,
        }
        referer = f"{self.base_url}/images/search?insightsToken={bcid}"
        image_info = {"imageInfo": {"imageInsightsToken": bcid, "source": "Gallery"}}

        # Build headers with signature if available
        headers = {"Referer": referer}
        if self._image_signature:
            headers["X-Image-Knowledge-Signature"] = self._image_signature

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
            ValueError: If the BCID or the image signature cannot be found on the search page.

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
            resp = await self._send_request(method="GET", url=resp_url)
            resp_json = await self._get_insights(bcid=self._parse_search_page(resp))

        elif file:
            # Upload image and get insights using BCID
            bcid, resp_url = await self._upload_image(file)
            resp_json = await self._get_insights(bcid=bcid)
        else:
            raise ValueError("Either 'url' or 'file' must be provided")

        return BingResponse(resp_json, resp_url)
