from pathlib import Path

import aiofiles
import httpx


class Network:
    def __init__(
        self,
        limit=30,
        max_connections=100,
        timeout=20,
        env=False,
        internal=False,
        proxies=None,
    ):
        """

        :param limit:
        :param max_connections:
        :param timeout:
        :param env:  debug输出:HTTPX_LOG_LEVEL=debug
        :param internal:
        :param proxies:
        """
        self.proxies = proxies
        self.internal = internal
        self.client = httpx.AsyncClient(
            verify=False,
            timeout=httpx.Timeout(timeout, connect=60),
            proxies=self.proxies,
            limits=httpx.Limits(
                max_keepalive_connections=limit, max_connections=max_connections
            ),
            trust_env=env,
            follow_redirects=True,
            event_hooks={"response": [raise_on_4xx_5xx]},
        )

    def start(self):
        return self.client

    async def close(self):
        await self.client.aclose()

    async def __aenter__(self):
        return self.client

    async def __aexit__(self, exc_type, exc, tb):
        await self.client.aclose()


async def raise_on_4xx_5xx(response: httpx.Response):
    if 400 <= response.status_code <= 599:
        response.raise_for_status()


class ClientManager:
    def __init__(self, session, env, proxies):
        self.session = (
            Network(internal=True, env=env, proxies=proxies) if not session else session
        )

    async def __aenter__(self):
        if isinstance(self.session, Network):
            return self.session.start()
        if isinstance(self.session, httpx.AsyncClient):
            return self.session

    async def __aexit__(self, exc_type, exc, tb):
        if isinstance(self.session, Network) and self.session.internal:
            await self.session.close()


class HandOver:
    def __init__(self, client=None, env=False, proxies=None, **requests_kwargs):
        self.session = client
        self.env = env
        self.proxies = proxies
        self.requests_kwargs = requests_kwargs

    async def get(self, _url, _headers=None, _params=None) -> httpx.Response:
        async with ClientManager(self.session, self.env, self.proxies) as session:
            res = await session.get(_url, headers=_headers, params=_params)
            return res

    async def post(
        self, _url, _headers=None, _params=None, _data=None, _json=None, _files=None
    ) -> httpx.Response:
        async with ClientManager(self.session, self.env, self.proxies) as session:
            if _json:
                res = await session.post(
                    _url, headers=_headers, params=_params, json=_json
                )
            elif _files:
                res = await session.post(
                    _url, headers=_headers, params=_params, files=_files
                )
            else:
                res = await session.post(
                    _url, headers=_headers, params=_params, data=_data
                )
            return res

    async def downloader(self, url="", path=None, filename="") -> Path:  # 下载器
        async with ClientManager(self.session, self.env, self.proxies) as session:
            async with session.stream("GET", url=url) as r:
                if path:
                    file = Path(path).joinpath(filename)
                else:
                    file = Path().cwd().joinpath(filename)
                async with aiofiles.open(file, "wb") as out_file:
                    async for chunk in r.aiter_bytes():
                        await out_file.write(chunk)
                return file
