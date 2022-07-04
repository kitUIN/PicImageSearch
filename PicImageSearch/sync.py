"""
From: telethon/sync
This magical module will rewrite all public methods in the public interface
of the library so they can run the loop on their own if it's not already
running. This rewrite may not be desirable if the end user always uses the
methods they way they should be ran, but it's incredibly useful for quick
scripts and the runtime overhead is relatively low.
"""
import asyncio
import functools
import inspect

from . import Ascii2D, BaiDu, EHentai, Google, Iqdb, Network, SauceNAO, TraceMoe


def _syncify_wrap(t, method_name):  # type: ignore
    method = getattr(t, method_name)

    @functools.wraps(method)
    def syncified(*args, **kwargs):  # type: ignore
        coro = method(*args, **kwargs)
        loop = asyncio.get_event_loop()
        return coro if loop.is_running() else loop.run_until_complete(coro)

    # Save an accessible reference to the original method
    setattr(syncified, "__tl.sync", method)
    setattr(t, method_name, syncified)


def syncify(*types):  # type: ignore
    for t in types:
        for name in dir(t):
            if (
                not name.startswith("_") or name == "__call__"
            ) and inspect.iscoroutinefunction(getattr(t, name)):
                _syncify_wrap(t, name)  # type: ignore


syncify(Ascii2D, BaiDu, EHentai, Google, Iqdb, Network, SauceNAO, TraceMoe)  # type: ignore

__all__ = [
    "Ascii2D",
    "BaiDu",
    "EHentai",
    "Google",
    "Iqdb",
    "Network",
    "SauceNAO",
    "TraceMoe",
]
