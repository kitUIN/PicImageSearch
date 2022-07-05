import asyncio
import logging as logger
import re
import socket
from json import loads as json_loads
from typing import Any, Dict, List, Optional, Set

from aiohttp import ClientSession, ClientTimeout
from aiohttp.abc import AbstractResolver


class DNSError(Exception):
    pass


class ByPassResolver(AbstractResolver):
    def __init__(
        self,
        endpoints: Optional[List[str]] = None,
    ) -> None:
        self.endpoints = endpoints or [
            "https://1.0.0.1/dns-query",
            "https://1.1.1.1/dns-query",
            "https://dns.alidns.com/resolve",
            "https://doh.dns.sb/dns-query",
            "https://cloudflare-dns.com/dns-query",
        ]

    async def resolve(
        self, hostname: str, port: int = 0, family: int = socket.AF_INET
    ) -> List[Dict[str, Any]]:
        tasks = [
            self._resolve(endpoint, hostname, family) for endpoint in self.endpoints
        ]
        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

        ips = await self.read_result(done.union(pending))
        for future in pending:
            future.cancel()

        if len(ips) == 0:
            raise DNSError(f"Failed to resolve {hostname}")

        return [
            {
                "hostname": hostname,
                "host": i,
                "port": port,
                "family": family,
                "proto": 0,
                "flags": socket.AI_NUMERICHOST,
            }
            for i in ips
        ]

    async def read_result(self, tasks: Set[asyncio.Task[Any]]) -> Any:
        if not tasks:
            return []
        task = tasks.pop()

        try:
            await task
            return task.result()
        except Exception as e:
            logger.error(f"caught: {repr(e)}")
            return await self.read_result(tasks)

    async def close(self) -> None:
        pass

    @staticmethod
    def parse_result(hostname: str, data: Dict[str, Any]) -> List[str]:
        if data["Status"] != 0:
            raise DNSError(f"Failed to resolve {hostname}")

        # Pattern to match IPv4 addresses
        pattern = re.compile(
            r"((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.){3}(1\d\d|2[0-4]\d|25[0-5]|[1-9]\d|\d)"
        )
        result = []

        for i in data["Answer"]:
            ip = i["data"]

            if pattern.match(ip) is not None:
                result.append(ip)

        return result

    async def _resolve(
        self, endpoint: str, hostname: str, family: int, timeout: int = 5
    ) -> List[str]:

        params = {
            "name": hostname,
            "type": "AAAA" if family == socket.AF_INET6 else "A",
            "do": "false",
            "cd": "false",
        }

        async with ClientSession() as session:
            async with session.get(
                endpoint,
                params=params,
                headers={"accept": "application/dns-json"},
                timeout=ClientTimeout(total=timeout),
            ) as resp:
                if resp.status == 200:
                    return self.parse_result(hostname, json_loads(await resp.text()))
                else:
                    raise DNSError(
                        f"Failed to resolve {hostname} with {endpoint}: HTTP Status {resp.status}"
                    )
