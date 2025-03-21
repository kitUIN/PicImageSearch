from types import TracebackType
from typing import Any, NamedTuple, Optional, Union

from httpx import AsyncClient, QueryParams, create_ssl_context

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/99.0.4844.82 Safari/537.36"
    )
}


class Network:
    """A class that manages HTTP client lifecycle and configuration.

    This class provides a wrapper around httpx.AsyncClient with support for
    cookies parsing, proxy configuration, and custom headers management.

    Attributes:
        internal (bool): Controls whether the client lifecycle is managed internally.
        cookies (dict[str, str]): Parsed cookies from the input string.
        client (AsyncClient): The underlying HTTP client instance.
    """

    def __init__(
        self,
        internal: bool = False,
        proxies: Optional[str] = None,
        headers: Optional[dict[str, str]] = None,
        cookies: Optional[str] = None,
        timeout: float = 30,
        verify_ssl: bool = True,
        http2: bool = False,
    ):
        """Initialize a new Network instance with custom configuration.

        Args:
            internal (bool): If True, manages its own client lifecycle.
            proxies (Optional[str]): Proxy URL string (e.g., "http://proxy.example.com:8080").
            headers (Optional[dict[str, str]]): Custom HTTP headers to merge with defaults.
            cookies (Optional[str]): Cookies in string format (e.g., "key1=value1; key2=value2").
            timeout (float): Request timeout in seconds.
            verify_ssl (bool): If True, verifies SSL certificates.
            http2 (bool): If True, enables HTTP/2 support.
        """
        self.internal: bool = internal
        headers = {**DEFAULT_HEADERS, **headers} if headers else DEFAULT_HEADERS
        self.cookies: dict[str, str] = {}
        if cookies:
            for line in cookies.split(";"):
                key, value = line.strip().split("=", 1)
                self.cookies[key] = value

        ssl_context = create_ssl_context(verify=verify_ssl)
        ssl_context.set_ciphers("DEFAULT")
        self.client: AsyncClient = AsyncClient(
            headers=headers,
            cookies=self.cookies,
            verify=ssl_context,
            http2=http2,
            proxy=proxies,
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
    """A context manager for HTTP client lifecycle management.

    This class provides a convenient way to manage HTTP client instances,
    either using an existing client or creating a new one with custom configuration.

    Attributes:
        client (Union[Network, AsyncClient]): The managed HTTP client instance.
    """

    def __init__(
        self,
        client: Optional[AsyncClient] = None,
        proxies: Optional[str] = None,
        headers: Optional[dict[str, str]] = None,
        cookies: Optional[str] = None,
        timeout: float = 30,
        verify_ssl: bool = True,
        http2: bool = False,
    ):
        """Initialize a ClientManager with an existing client or create a new one.

        Args:
            client (Optional[AsyncClient]): An existing AsyncClient instance or None to create a new one.
            proxies (Optional[str]): Proxy URL string for the new client.
            headers (Optional[dict[str, str]]): Custom headers for the new client.
            cookies (Optional[str]): Cookies string for the new client.
            timeout (float): Request timeout in seconds.
            verify_ssl (bool): If True, verifies SSL certificates.
            http2 (bool): If True, enables HTTP/2 support.

        Note:
            If client is provided, other parameters are ignored.
        """
        self.client: Union[Network, AsyncClient] = client or Network(
            internal=True,
            proxies=proxies,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            verify_ssl=verify_ssl,
            http2=http2,
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


class RESP(NamedTuple):
    """A named tuple for HTTP response data.

    This class provides a convenient way to store and access HTTP response data,
    including the response body, URL, and status code.

    Attributes:
        text (str): The response body as text.
        url (str): The final URL after any redirects.
        status_code (int): The HTTP status code.
    """

    text: str
    url: str
    status_code: int


class HandOver:
    """A high-level interface for making HTTP requests.

    This class provides convenient methods for making HTTP requests with automatic
    client lifecycle management. It supports GET, POST, and download operations.

    Attributes:
        client (Optional[AsyncClient]): An optional pre-configured client.
        proxies (Optional[str]): Proxy settings for requests.
        headers (Optional[dict]): Default headers for requests.
        cookies (Optional[str]): Default cookies for requests.
        timeout (float): Default timeout for requests.
        verify_ssl (bool): If True, verifies SSL certificates.
        http2 (bool): If True, enables HTTP/2 support.
    """

    def __init__(
        self,
        client: Optional[AsyncClient] = None,
        proxies: Optional[str] = None,
        headers: Optional[dict[str, str]] = None,
        cookies: Optional[str] = None,
        timeout: float = 30,
        verify_ssl: bool = True,
        http2: bool = False,
    ):
        """Initializes HandOver with an existing AsyncClient or creates a new one.

        Args:
            client (Optional[AsyncClient]): An existing AsyncClient instance or None for a new client.
            proxies (Optional[str]): Proxy settings.
            headers (Optional[dict[str, str]]): Custom headers.
            cookies (Optional[str]): Cookies in ';' separated string format.
            timeout (float): Timeout duration.
            verify_ssl (bool): If True, verifies SSL certificates.
            http2 (bool): If True, enables HTTP/2 support.
        """
        self.client: Optional[AsyncClient] = client
        self.proxies: Optional[str] = proxies
        self.headers: Optional[dict[str, str]] = headers
        self.cookies: Optional[str] = cookies
        self.timeout: float = timeout
        self.verify_ssl: bool = verify_ssl
        self.http2: bool = http2

    async def get(
        self,
        url: str,
        params: Optional[dict[str, str]] = None,
        headers: Optional[dict[str, str]] = None,
        **kwargs: Any,
    ) -> RESP:
        """Perform an HTTP GET request with automatic client management.

        Args:
            url (str): The target URL for the GET request.
            params (Optional[dict[str, str]]): Optional query parameters to append to the URL.
            headers (Optional[dict[str, str]]): Optional headers to override defaults.
            **kwargs (Any): Additional arguments passed to httpx.AsyncClient.get().

        Returns:
            RESP: A named tuple containing:
                - text: The response body as text
                - url: The final URL after any redirects
                - status_code: The HTTP status code

        Note:
            The client is automatically managed within a context manager.
        """
        async with ClientManager(
            self.client,
            self.proxies,
            self.headers,
            self.cookies,
            self.timeout,
            self.verify_ssl,
            self.http2,
        ) as client:
            resp = await client.get(url, params=params, headers=headers, **kwargs)
            return RESP(resp.text, str(resp.url), resp.status_code)

    async def post(
        self,
        url: str,
        params: Union[dict[str, Any], QueryParams, None] = None,
        headers: Optional[dict[str, str]] = None,
        data: Optional[dict[Any, Any]] = None,
        files: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ) -> RESP:
        """Perform an HTTP POST request with automatic client management.

        Args:
            url (str): The target URL for the POST request.
            params (Union[dict[str, Any], QueryParams, None]): Query parameters or QueryParams object.
            headers (Optional[dict[str, str]]): Optional headers to override defaults.
            data (Optional[dict[Any, Any]]): Optional form data for the request body.
            files (Optional[dict[str, Any]]): Optional files for multipart/form-data requests.
            json (Optional[dict[str, Any]]): Optional JSON data for the request body.
            **kwargs (Any): Additional arguments passed to httpx.AsyncClient.post().

        Returns:
            RESP: A dataclass containing:
                - text: The response body as text
                - url: The final URL after any redirects
                - status_code: The HTTP status code

        Note:
            - Only one of `data`, `files`, or `json` should be provided.
            - The client is automatically managed within a context manager.
        """
        async with ClientManager(
            self.client,
            self.proxies,
            self.headers,
            self.cookies,
            self.timeout,
            self.verify_ssl,
            self.http2,
        ) as client:
            resp = await client.post(
                url,
                params=params,
                headers=headers,
                data=data,
                files=files,
                json=json,
                **kwargs,
            )
            return RESP(resp.text, str(resp.url), resp.status_code)

    async def download(self, url: str, headers: Optional[dict[str, str]] = None) -> bytes:
        """Download content from a URL with automatic client management.

        Args:
            url (str): The URL to download content from.
            headers (Optional[dict[str, str]]): Optional headers to override defaults.

        Returns:
            bytes: The downloaded content as bytes.

        Note:
            The client is automatically managed within a context manager.
        """
        async with ClientManager(
            self.client,
            self.proxies,
            self.headers,
            self.cookies,
            self.timeout,
            self.verify_ssl,
            self.http2,
        ) as client:
            resp = await client.get(url, headers=headers)
            return resp.read()
