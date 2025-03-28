from json import loads as json_loads
from pathlib import Path
from typing import Any, Optional, Union

from lxml.html import HTMLParser, fromstring
from pyquery import PyQuery
from typing_extensions import override

from ..model import BaiDuResponse
from ..utils import deep_get, read_file
from .base import BaseSearchEngine


class BaiDu(BaseSearchEngine[BaiDuResponse]):
    """API client for the BaiDu image search engine.

    Used for performing reverse image searches using BaiDu service.

    Attributes:
        base_url (str): The base URL for BaiDu searches.
    """

    def __init__(self, **request_kwargs: Any):
        """Initializes a BaiDu API client with specified configurations.

        Args:
            **request_kwargs (Any): Additional arguments for network requests.
        """
        base_url = "https://graph.baidu.com"
        super().__init__(base_url, **request_kwargs)

    @staticmethod
    def _extract_card_data(data: PyQuery) -> list[dict[str, Any]]:
        """Extracts 'window.cardData' from the BaiDu search response page.

        This method parses the JavaScript content in the page to find and extract
        the 'window.cardData' object, which contains the search results.

        Args:
            data (PyQuery): A PyQuery object containing the parsed HTML page.

        Returns:
            list[dict[str, Any]]: A list of card data dictionaries, where each dictionary
                contains information about a search result. Returns an empty list if
                no card data is found.

        Note:
            The method searches for specific script tags containing 'window.cardData'
            and extracts the JSON data between the first '[' and last ']' characters.
        """
        for script in data("script").items():
            script_text = script.text()
            if script_text and "window.cardData" in script_text:
                start = script_text.find("[")
                end = script_text.rfind("]") + 1
                return json_loads(script_text[start:end])
        return []

    @override
    async def search(
        self,
        url: Optional[str] = None,
        file: Union[str, bytes, Path, None] = None,
        **kwargs: Any,
    ) -> BaiDuResponse:
        """Performs a reverse image search on BaiDu.

        This method supports two ways of searching:
            1. Search by image URL
            2. Search by uploading a local image file

        The search process involves multiple steps:
            1. Upload the image or submit the URL to BaiDu
            2. Follow the returned URL to get the search results page
            3. Extract and parse the card data from the page
            4. If similar images are found, fetch the detailed results

        Args:
            url (Optional[str]): URL of the image to search.
            file (Union[str, bytes, Path, None]): Local image file, can be a path string, bytes data, or Path object.
            **kwargs (Any): Additional arguments passed to the parent class.

        Returns:
            BaiDuResponse: An object containing the search results and metadata.
                Returns empty results if no matches are found or if the 'noresult'
                card is present.

        Raises:
            ValueError: If neither `url` nor `file` is provided.

        Note:
            - Only one of `url` or `file` should be provided.
            - The search process involves multiple HTTP requests to BaiDu's API.
            - The response format varies depending on whether matches are found.
        """
        data = {"from": "pc"}

        if url:
            files = {"image": await self.download(url)}
        elif file:
            files = {"image": read_file(file)}
        else:
            raise ValueError("Either 'url' or 'file' must be provided")

        resp = await self._send_request(
            method="post",
            endpoint="upload",
            headers={"Acs-Token": ""},
            data=data,
            files=files,
        )
        data_url = deep_get(json_loads(resp.text), "data.url")
        if not data_url:
            return BaiDuResponse({}, resp.url)

        resp = await self._send_request(method="get", url=data_url)

        utf8_parser = HTMLParser(encoding="utf-8")
        data = PyQuery(fromstring(resp.text, parser=utf8_parser))
        card_data = self._extract_card_data(data)
        same_data = None

        for card in card_data:
            if card.get("cardName") == "noresult":
                return BaiDuResponse({}, data_url)
            if card.get("cardName") == "same":
                same_data = card["tplData"]
            if card.get("cardName") == "simipic":
                next_url = card["tplData"]["firstUrl"]
                resp = await self._send_request(method="get", url=next_url)
                resp_data = json_loads(resp.text)

                if same_data:
                    resp_data["same"] = same_data

                return BaiDuResponse(resp_data, data_url)

        return BaiDuResponse({}, data_url)
