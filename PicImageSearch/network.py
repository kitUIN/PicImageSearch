from collections import namedtuple
from types import TracebackType
from typing import Any, Optional, Union

from httpx import AsyncClient, QueryParams

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/99.0.4844.82 Safari/537.36"
    )
}
RESP = namedtuple("RESP", ["text", "url", "status_code"])


class Network:
    """Manages HTTP client for network operations.

    Attributes:
        internal: Indicates if the object manages its own client lifecycle.
        cookies: Dictionary of parsed cookies, provided in string format upon initialization.
        client: Instance of an HTTP client.
    """

    def __init__(
        self,
        internal: bool = False,
        proxies: Optional[str] = None,
        headers: Optional[dict[str, str]] = None,
        cookies: Optional[str] = None,
        timeout: float = 30,
        verify_ssl: bool = True,
    ):
        """Initializes Network with configuration for HTTP requests.

        Args:
            internal: If True, Network manages its own HTTP client lifecycle.
            proxies: Proxy settings for the HTTP client.
            headers: Custom headers for the HTTP client.
            cookies: Cookies in string format for the HTTP client.
            timeout: Timeout duration for the HTTP client.
            verify_ssl: If True, verifies SSL certificates.
        """
        self.internal: bool = internal
        headers = {**DEFAULT_HEADERS, **headers} if headers else DEFAULT_HEADERS
        self.cookies: dict[str, str] = {}
        if cookies:
            for line in cookies.split(";"):
                key, value = line.strip().split("=", 1)
                self.cookies[key] = value

        self.client: AsyncClient = AsyncClient(
            headers=headers,
            cookies=self.cookies,
            verify=verify_ssl,
            proxies=proxies,
            timeout=timeout,
            follow_redirects=True,
        )

    def start(self) -> AsyncClient:
        """Initializes and returns the HTTP client.

        Returns:
            AsyncClient: Initialized HTTP client for network operations.
        """
        return self.client

    async def close(self) -> None:
        """Closes the HTTP client session if managed internally."""
        await self.client.aclose()

    async def __aenter__(self) -> AsyncClient:
        """Async context manager entry for initializing or returning the HTTP client.

        Returns:
            AsyncClient: The HTTP client instance.
        """
        return self.client

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]] = None,
        exc_val: Optional[BaseException] = None,
        exc_tb: Optional[TracebackType] = None,
    ) -> None:
        """Async context manager exit for closing the HTTP client if managed internally."""
        await self.client.aclose()


class ClientManager:
    """Manages an HTTP client for network requests, handling lifecycle if created internally.

    Attributes:
        client: Managed instance of the HTTP client.
    """

    def __init__(
        self,
        client: Optional[AsyncClient] = None,
        proxies: Optional[str] = None,
        headers: Optional[dict[str, str]] = None,
        cookies: Optional[str] = None,
        timeout: float = 30,
    ):
        """Initializes ClientManager with an existing HTTP client or creates a new one.

        Args:
            client: An existing AsyncClient instance or None to create a new one.
            proxies: Proxy settings for the new client.
            headers: Custom headers for the new client.
            cookies: Cookies in ';' separated string format for the new client.
            timeout: Timeout setting for the new client.
        """
        self.client: Union[Network, AsyncClient] = client or Network(
            internal=True,
            proxies=proxies,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
        )

    async def __aenter__(self) -> AsyncClient:
        """Async context manager entry for network operations with new or existing client.

        Returns:
            AsyncClient: The instance ready for use.
        """
        return self.client.start() if isinstance(self.client, Network) else self.client

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]] = None,
        exc_val: Optional[BaseException] = None,
        exc_tb: Optional[TracebackType] = None,
    ) -> None:
        """Async context manager exit, cleans up the client if created internally."""
        if isinstance(self.client, Network) and self.client.internal:
            await self.client.close()


class HandOver:
    """Facilitates network operations like GET, POST, and download, managing an HTTP client.

    Provides methods for HTTP GET, POST requests, and download operations,
    managing the lifecycle of an HTTP client.

    Attributes:
        client: Optional pre-configured AsyncClient instance.
        proxies: Proxy settings for requests.
        headers: Custom HTTP headers for requests.
        cookies: Cookies for requests in string format.
        timeout: Timeout duration for requests.
    """

    def __init__(
        self,
        client: Optional[AsyncClient] = None,
        proxies: Optional[str] = None,
        headers: Optional[dict[str, str]] = None,
        cookies: Optional[str] = None,
        timeout: float = 30,
    ):
        """Initializes HandOver with an existing AsyncClient or creates a new one.

        Args:
            client: An existing AsyncClient or None for a new client.
            proxies: Proxy settings.
            headers: Custom headers.
            cookies: Cookies in ';' separated string format.
            timeout: Timeout duration.
        """
        self.client: Optional[AsyncClient] = client
        self.proxies: Optional[str] = proxies
        self.headers: Optional[dict[str, str]] = headers
        self.cookies: Optional[str] = cookies
        self.timeout: float = timeout

    async def get(
        self, url: str, params: Optional[dict[str, str]] = None, **kwargs: Any
    ) -> RESP:
        """Performs an HTTP GET request.

        Args:
            url: URL for the GET request.
            params: Optional query parameters.
            **kwargs: Additional arguments for the GET request.

        Returns:
            RESP: Response with text, URL, and status code.
        """
        async with ClientManager(
            self.client,
            self.proxies,
            self.headers,
            self.cookies,
            self.timeout,
        ) as client:
            resp = await client.get(url, params=params, **kwargs)
            return RESP(resp.text, str(resp.url), resp.status_code)

    async def post(
        self,
        url: str,
        params: Union[dict[str, Any], QueryParams, None] = None,
        data: Optional[dict[Any, Any]] = None,
        files: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ) -> RESP:
        """Performs an HTTP POST request.

        Args:
            url: URL for the POST request.
            params: Optional query or QueryParams object.
            data: Optional data for the request body.
            files: Optional file-like objects for multipart submissions.
            json: Optional JSON payload for the request body.
            **kwargs: Additional arguments for the POST request.

        Returns:
            RESP: Response with text, URL, and status code.
        """
        async with ClientManager(
            self.client,
            self.proxies,
            self.headers,
            self.cookies,
            self.timeout,
        ) as client:
            resp = await client.post(
                url, params=params, data=data, files=files, json=json, **kwargs
            )
            return RESP(resp.text, str(resp.url), resp.status_code)

    async def download(self, url: str) -> bytes:
        """Downloads content from a URL.

        Args:
            url: URL to download content from.

        Returns:
            bytes: Downloaded content.
        """
        async with ClientManager(
            self.client,
            self.proxies,
            self.headers,
            self.cookies,
            self.timeout,
        ) as client:
            resp = await client.get(url)
            return resp.read()
