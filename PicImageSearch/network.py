from collections import namedtuple
from types import TracebackType
from typing import Any, Dict, Optional, Type, Union

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
    """Creates and manages the HTTP client used for network operations.

    Attributes:
        internal: A flag indicating whether the object should manage its own client lifecycle.
        cookies: A dictionary that holds parsed cookies if provided in string format on initialization.
    """

    def __init__(
        self,
        internal: bool = False,
        proxies: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[str] = None,
        timeout: float = 30,
        verify_ssl: bool = True,
    ):
        """Initializes the Network object with configuration for the HTTP client.

        Args:
            internal: Specifies if the client should be managed internally.
            proxies: The proxy configuration to be used with the HTTP client.
            headers: Custom headers to be used with the HTTP client.
            cookies: Cookies to be used with the HTTP client in a ';' separated string format.
            timeout: The timeout to use for network operations.
            verify_ssl: A flag to indicate whether to verify SSL certificates.
        """
        self.internal: bool = internal
        headers = {**DEFAULT_HEADERS, **headers} if headers else DEFAULT_HEADERS
        self.cookies: Dict[str, str] = {}
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
        """Starts and returns the internally managed HTTP client.

        Returns:
            The initialized AsyncClient instance.
        """
        return self.client

    async def close(self) -> None:
        """Closes the internally managed HTTP client session."""
        await self.client.aclose()

    async def __aenter__(self) -> AsyncClient:
        """Async context manager entry, initializing or returning the HTTP client.

        Returns:
            The initialized AsyncClient instance if managed internally, otherwise the predefined client.
        """
        return self.client

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]] = None,
        exc_val: Optional[BaseException] = None,
        exc_tb: Optional[TracebackType] = None,
    ) -> None:
        """Async context manager exit, closing the HTTP client if it is managed internally."""
        await self.client.aclose()


class ClientManager:
    """Manages an HTTP client for performing network requests, handling the lifecycle if created internally.

    Attributes:
        client: The HTTP client to be managed.
    """

    def __init__(
        self,
        client: Optional[AsyncClient] = None,
        proxies: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[str] = None,
        timeout: float = 30,
    ):
        """Initializes the ClientManager with an existing client or new client configuration.

        Args:
            client: A pre-configured AsyncClient instance if available, otherwise None.
            proxies: The proxy configuration for a new client if required.
            headers: Custom headers for a new client if required.
            cookies: Cookies in a ';' separated string format for a new client if provided.
            timeout: Timeout for the new client if created.
        """
        self.client: Union[Network, AsyncClient] = client or Network(
            internal=True,
            proxies=proxies,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
        )

    async def __aenter__(self) -> AsyncClient:
        """Async context manager entry for performing network operations, starting a new client or using an existing one

        Returns:
            The instance of AsyncClient ready for use.
        """
        return self.client.start() if isinstance(self.client, Network) else self.client

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]] = None,
        exc_val: Optional[BaseException] = None,
        exc_tb: Optional[TracebackType] = None,
    ) -> None:
        """Async context manager exit, cleaning up the client if it was created internally."""
        if isinstance(self.client, Network) and self.client.internal:
            await self.client.close()


class HandOver:
    """Facilitates network operations like GET, POST, and download, reusing or creating an HTTP client accordingly.

    Attributes:
        client: A pre-configured AsyncClient instance if available, otherwise None.
        proxies: The proxy configuration for a new client if required.
        headers: Custom headers for a new client if required.
        cookies: Cookies in a ';' separated string format for a new client if provided.
        timeout: Timeout for the new client if created.
    """

    def __init__(
        self,
        client: Optional[AsyncClient] = None,
        proxies: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[str] = None,
        timeout: float = 30,
    ):
        """Initializes the HandOver with or without a pre-configured AsyncClient.

        Args:
            client: An existing AsyncClient to be reused, otherwise None.
            proxies: Proxies for a new client if required.
            headers: Custom headers for a new client if required.
            cookies: Cookies in a ';' separated string format for a new client if provided.
            timeout: Timeout for a new client if created.
        """
        self.client: Optional[AsyncClient] = client
        self.proxies: Optional[str] = proxies
        self.headers: Optional[Dict[str, str]] = headers
        self.cookies: Optional[str] = cookies
        self.timeout: float = timeout

    async def get(
        self, url: str, params: Optional[Dict[str, str]] = None, **kwargs: Any
    ) -> RESP:
        """Performs an HTTP GET request.

        Args:
            url: The URL to perform the GET request on.
            params: Optional dictionary of URL parameters to append to the URL.
            **kwargs: Additional keyword arguments passed to the GET request method.

        Returns:
            A namedtuple RESP with response text, response URL, and status code.
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
        params: Union[Dict[str, Any], QueryParams, None] = None,
        data: Optional[Dict[Any, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> RESP:
        """Performs an HTTP POST request.

        Args:
            url: The URL to perform the POST request on.
            params: Optional dictionary or QueryParams object of URL parameters.
            data: Optional dictionary of form data to send in the body of the request.
            files: Optional dictionary of file-like objects to send in the multipart request.
            json: Optional dictionary which if given, will be sent as a JSON payload.
            **kwargs: Additional keyword arguments passed to the POST request method.

        Returns:
            A namedtuple RESP with response text, response URL, and status code.
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
        """Downloads content from a given URL.

        Args:
            url: The URL to download content from.

        Returns:
            The content of the response as bytes.
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
