from types import TracebackType
from typing import Any, Dict, Optional, Tuple, Type, Union

from aiohttp import ClientSession, ClientTimeout, FormData, TCPConnector
from multidict import MultiDict


class Network:
    def __init__(
        self,
        internal: bool = False,
        proxies: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[str] = None,
        bypass: bool = False,
    ):
        self.internal: bool = internal
        if not headers:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
            }
        self.cookies: Dict[str, str] = {}
        if cookies:
            for line in cookies.split(";"):
                key, value = line.strip().split("=", 1)
                self.cookies[key] = value
        kwargs = {}
        if bypass:
            import ssl

            from .bypass import ByPassResolver

            ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            ssl_ctx.check_hostname = False
            ssl_ctx.verify_mode = ssl.CERT_NONE

            kwargs.update({"ssl": ssl_ctx, "resolver": ByPassResolver()})

        self.conn = TCPConnector(**kwargs)  # type: ignore
        self.client: ClientSession = ClientSession(
            connector=self.conn,
            headers=headers,
            cookies=self.cookies,
            timeout=ClientTimeout(total=20.0),
        )
        if proxies:
            from functools import partial

            self.client.get = partial(self.client.get, proxy=proxies)  # type: ignore
            self.client.post = partial(self.client.post, proxy=proxies)  # type: ignore

    def start(self) -> ClientSession:
        return self.client

    async def close(self) -> None:
        await self.client.close()

    async def __aenter__(self) -> ClientSession:
        return self.client

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]] = None,
        exc_val: Optional[BaseException] = None,
        exc_tb: Optional[TracebackType] = None,
    ) -> None:
        await self.client.close()


class ClientManager:
    def __init__(
        self,
        client: Optional[ClientSession] = None,
        proxies: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[str] = None,
        bypass: bool = False,
    ):
        self.client: Union[Network, ClientSession] = client or Network(
            internal=True,
            proxies=proxies,
            headers=headers,
            cookies=cookies,
            bypass=bypass,
        )

    async def __aenter__(self) -> ClientSession:
        return self.client.start() if isinstance(self.client, Network) else self.client

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
        client: Optional[ClientSession] = None,
        proxies: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[str] = None,
        bypass: bool = False,
    ):
        self.client: Optional[ClientSession] = client
        self.proxies: Optional[str] = proxies
        self.headers: Optional[Dict[str, str]] = headers
        self.cookies: Optional[str] = cookies
        self.bypass: bool = bypass

    async def get(
        self, url: str, params: Optional[Dict[str, str]] = None, **kwargs: Any
    ) -> Tuple[str, str, int]:
        async with ClientManager(
            self.client, self.proxies, self.headers, self.cookies, self.bypass
        ) as client:
            async with client.get(url, params=params, **kwargs) as resp:
                return await resp.text(), str(resp.url), resp.status

    async def post(
        self,
        url: str,
        params: Union[Dict[str, Any], MultiDict[Union[str, int]], None] = None,
        data: Union[Dict[Any, Any], FormData, None] = None,
        json: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> Tuple[str, str, int]:
        async with ClientManager(
            self.client, self.proxies, self.headers, self.cookies, self.bypass
        ) as client:
            async with client.post(
                url, params=params, data=data, json=json, **kwargs
            ) as resp:
                return await resp.text(), str(resp.url), resp.status

    async def download(self, url: str) -> bytes:
        async with ClientManager(
            self.client, self.proxies, self.headers, self.cookies, self.bypass
        ) as client:
            async with client.get(url) as resp:
                return await resp.read()
