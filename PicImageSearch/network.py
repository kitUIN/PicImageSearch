from pathlib import Path
from types import TracebackType
from typing import IO, Any, Dict, Optional, Type, Union

import aiofiles
import httpx


class Network:
    def __init__(
        self,
        limit: int = 30,
        max_connections: int = 100,
        timeout: Optional[float] = 20,
        env: bool = False,
        internal: Optional[bool] = False,
        proxies: Optional[str] = None,
    ):
        """

        :param limit:
        :param max_connections:
        :param timeout:
        :param env:  debug输出:HTTPX_LOG_LEVEL=debug
        :param internal:
        :param proxies:
        """
        self.internal: Optional[int] = internal
        self.client: httpx.AsyncClient = httpx.AsyncClient(
            verify=False,
            timeout=httpx.Timeout(timeout, connect=60),
            proxies=proxies,  # type: ignore
            limits=httpx.Limits(
                max_keepalive_connections=limit, max_connections=max_connections
            ),
            trust_env=env,
            follow_redirects=True,
            event_hooks={"response": [raise_on_4xx_5xx]},
        )

    async def __aenter__(self) -> httpx.AsyncClient:
        return self.client

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]] = None,
        exc_value: Optional[BaseException] = None,
        traceback: Optional[TracebackType] = None,
    ) -> None:
        await self.client.aclose()


async def raise_on_4xx_5xx(response: httpx.Response) -> None:
    if 400 <= response.status_code <= 599:
        response.raise_for_status()


class ClientManager:
    def __init__(
        self,
        client: Optional[httpx.AsyncClient],
        proxies: Optional[str],
        env: bool = False,
    ):
        self.client: Union[Network, httpx.AsyncClient] = (
            Network(internal=True, env=env, proxies=proxies) if not client else client
        )

    async def __aenter__(self) -> httpx.AsyncClient:
        if isinstance(self.client, Network):
            return await self.client.__aenter__()
        return self.client

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]] = None,
        exc_value: Optional[BaseException] = None,
        traceback: Optional[TracebackType] = None,
    ) -> None:
        if isinstance(self.client, Network) and self.client.internal:
            await self.client.__aexit__(exc_type, exc_value, traceback)


class HandOver:
    def __init__(
        self,
        client: Optional[httpx.AsyncClient] = None,
        env: bool = False,
        proxies: Optional[str] = None,
        **requests_kwargs: Any
    ):
        self.client: Optional[httpx.AsyncClient] = client
        self.env: bool = env
        self.proxies: Optional[str] = proxies
        self.requests_kwargs: Dict[str, Any] = (
            requests_kwargs if requests_kwargs else {}
        )

    async def get(
        self,
        _url: str,
        _headers: Optional[Dict[str, str]] = None,
        _params: Optional[Dict[str, Any]] = None,
    ) -> httpx.Response:
        async with ClientManager(self.client, self.proxies, self.env) as session:
            return await session.get(_url, headers=_headers, params=_params)  # type: ignore

    async def post(
        self,
        _url: str,
        _headers: Optional[Dict[str, str]] = None,
        _params: Optional[Dict[str, Any]] = None,
        _data: Optional[Dict[Any, Any]] = None,
        _json: Optional[Dict[str, str]] = None,
        _files: Optional[Dict[str, Any]] = None,
    ) -> httpx.Response:
        async with ClientManager(self.client, self.proxies, self.env) as session:
            return await session.post(
                _url,
                headers=_headers,  # type: ignore
                params=_params,
                data=_data,  # type: ignore
                files=_files,  # type: ignore
                json=_json,
            )

    async def downloader(
        self, url: str, filename: str, path: Optional[str] = None
    ) -> Path:  # 下载器
        async with ClientManager(self.client, self.proxies, self.env) as session:
            async with session.stream("GET", url=url) as r:
                if path:
                    file = Path(path).joinpath(filename)
                else:
                    file = Path().cwd().joinpath(filename)
                async with aiofiles.open(file, "wb") as out_file:
                    async for chunk in r.aiter_bytes():
                        await out_file.write(chunk)
                return file
