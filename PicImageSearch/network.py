from types import TracebackType
from typing import Any, Dict, Optional, Type, Union

from httpx import AsyncClient, AsyncHTTPTransport, Response


class Network:
    def __init__(
        self,
        internal: bool = False,
        proxies: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[str] = None,
    ):
        self.internal: bool = internal
        if not headers:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
            }
        else:
            headers.update(headers)
        self.cookies: Dict[str, str] = {}
        if cookies:
            for line in cookies.split(";"):
                key, value = line.strip().split("=", 1)
                self.cookies[key] = value
        transport = AsyncHTTPTransport(verify=False, retries=3)
        self.client: AsyncClient = AsyncClient(
            proxies=proxies,  # type: ignore
            headers=headers,
            cookies=self.cookies,
            timeout=10.0,
            follow_redirects=True,
            transport=transport,
        )

    def start(self) -> AsyncClient:
        return self.client

    async def close(self) -> None:
        await self.client.aclose()

    async def __aenter__(self) -> AsyncClient:
        return self.client

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]] = None,
        exc_val: Optional[BaseException] = None,
        exc_tb: Optional[TracebackType] = None,
    ) -> None:
        await self.client.aclose()


class ClientManager:
    def __init__(
        self,
        client: Optional[AsyncClient] = None,
        proxies: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[str] = None,
    ):
        self.client: Union[Network, AsyncClient] = (
            Network(internal=True, proxies=proxies, headers=headers, cookies=cookies)
            if client is None
            else client
        )

    async def __aenter__(self) -> AsyncClient:
        if isinstance(self.client, Network):
            return self.client.start()
        return self.client

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]] = None,
        exc_val: Optional[BaseException] = None,
        exc_tb: Optional[TracebackType] = None,
    ) -> None:
        if isinstance(self.client, Network) and self.client.internal:
            await self.client.close()


class HandOver:
    def __init__(
        self,
        client: Optional[AsyncClient] = None,
        proxies: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[str] = None,
    ):
        self.client: Optional[AsyncClient] = client
        self.proxies: Optional[str] = proxies
        self.headers: Optional[Dict[str, str]] = headers
        self.cookies: Optional[str] = cookies

    async def get(
        self, url: str, params: Optional[Dict[str, str]] = None, **kwargs: Any
    ) -> Response:
        async with ClientManager(
            self.client, self.proxies, self.headers, self.cookies
        ) as client:
            return await client.get(url, params=params, **kwargs)

    async def post(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[Any, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> Response:
        async with ClientManager(
            self.client, self.proxies, self.headers, self.cookies
        ) as client:
            return await client.post(
                url, params=params, data=data, files=files, json=json, **kwargs  # type: ignore
            )
