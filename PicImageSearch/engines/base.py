from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Generic, Optional, TypeVar, Union

from ..model.base import BaseSearchResponse
from ..network import RESP, HandOver

ResponseT = TypeVar("ResponseT")
T = TypeVar("T", bound=BaseSearchResponse[Any])


class BaseSearchEngine(HandOver, ABC, Generic[T]):
    """Base search engine class providing common functionality for all reverse image search engines.

    This abstract base class implements the core functionality shared by all image search engines,
    including network request handling and basic parameter validation.

    Attributes:
        base_url (str): The base URL endpoint for the search engine's API.
    """

    base_url: str

    def __init__(self, base_url: str, **request_kwargs: Any):
        """Initialize the base search engine.

        Args:
            base_url (str): The base URL for the search engine's API endpoint.
            **request_kwargs (Any): Additional parameters for network requests, such as:
                - headers: Custom HTTP headers
                - proxies: Proxy settings
                - timeout: Request timeout settings
                - etc.
        """
        super().__init__(**request_kwargs)
        self.base_url = base_url

    @abstractmethod
    async def search(
        self,
        url: Optional[str] = None,
        file: Union[str, bytes, Path, None] = None,
        **kwargs: Any,
    ) -> T:
        """Perform a reverse image search.

        This abstract method must be implemented by all search engine classes.
        Supports searching by either image URL or local file.

        Args:
            url (Optional[str]): URL of the image to search. Must be a valid HTTP/HTTPS URL.
            file (Union[str, bytes, Path, None]): Local image file to search. Can be:
                - A string path to the image
                - Raw bytes of the image
                - A Path object pointing to the image
            **kwargs (Any): Additional search parameters specific to each search engine.

        Returns:
            T: Search results. The specific return type depends on the implementing class.

        Raises:
            ValueError: If neither 'url' nor 'file' is provided.
            NotImplementedError: If the method is not implemented by the subclass.
        """
        raise NotImplementedError

    async def _send_request(self, method: str, endpoint: str = "", url: str = "", **kwargs: Any) -> RESP:
        """Send an HTTP request and return the response.

        A utility method that handles both GET and POST requests to the search engine's API.

        Args:
            method (str): HTTP method, must be either 'get' or 'post' (case-insensitive).
            endpoint (str): API endpoint to append to the base URL. If empty, uses base_url directly.
            url (str): Full URL for the request. Overrides base_url and endpoint if provided.
            **kwargs (Any): Additional parameters for the request, such as:
                - params: URL parameters for GET requests
                - data: Form data for POST requests
                - files: Files to upload
                - headers: Custom HTTP headers
                - etc.

        Returns:
            RESP: A dataclass containing:
                - text: The response body as text
                - url: The final URL after any redirects
                - status_code: The HTTP status code

        Raises:
            ValueError: If an unsupported HTTP method is specified.
        """
        request_url = url or (f"{self.base_url}/{endpoint}" if endpoint else self.base_url)

        method = method.lower()
        if method == "get":
            # Files are not valid for GET requests
            kwargs.pop("files", None)
            return await self.get(request_url, **kwargs)
        elif method == "post":
            return await self.post(request_url, **kwargs)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
