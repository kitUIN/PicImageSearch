from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional, TypeVar, Union

from ..network import HandOver

T = TypeVar("T")


class BaseSearchEngine(HandOver, ABC):
    """Base search engine class providing common functionality for all reverse image search engines."""

    def __init__(self, base_url: str, **request_kwargs: Any):
        """Initialize the base search engine.

        Args:
            base_url: The base URL for the search engine.
            **request_kwargs: Additional parameters for network requests.
        """
        super().__init__(**request_kwargs)
        self.base_url = base_url

    @abstractmethod
    async def search(
        self,
        url: Optional[str] = None,
        file: Union[str, bytes, Path, None] = None,
        **kwargs: Any,
    ) -> T:  # noqa
        """Perform a reverse image search.

        Args:
            url: URL of the image to search.
            file: Local image file to search (path or bytes).
            **kwargs: Other search parameters.

        Returns:
            T: Search results.

        Raises:
            ValueError: If neither 'url' nor 'file' is provided.
        """
        if not url and not file:
            raise ValueError("Either 'url' or 'file' must be provided")

    async def _make_request(
        self, method: str, endpoint: str = "", **kwargs: Any
    ) -> Any:
        """Send an HTTP request and return the response.

        Args:
            method: HTTP method ('get' or 'post').
            endpoint: API endpoint.
            **kwargs: Additional parameters for the request.

        Returns:
            Any: Request response.
        """
        url = f"{self.base_url}/{endpoint}" if endpoint else self.base_url

        if method.lower() == "get":
            if "files" in kwargs:
                kwargs.pop("files")
            return await self.get(url, **kwargs)
        elif method.lower() == "post":
            return await self.post(url, **kwargs)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
