"""From: telethon/sync
Rewrites all public asynchronous methods in the library's public interface for synchronous execution.
Useful for scripts, with low runtime overhead. Ideal for synchronous calls preference over managing an event loop.

Automatically wraps asynchronous methods of specified classes, enabling synchronous calls.
"""

import asyncio
import functools
import inspect

from . import (
    Ascii2D,
    BaiDu,
    Bing,
    Copyseeker,
    EHentai,
    Google,
    Iqdb,
    Network,
    SauceNAO,
    Tineye,
    TraceMoe,
    Yandex,
)


def _syncify_wrap(class_type, method_name):  # type: ignore
    """Wrap an asynchronous method of a class for synchronous calling.

    Creates a synchronous version of the specified asynchronous method.
    Checks if the event loop is running; if not, runs it until method completion.
    Original asynchronous method remains accessible via `__tl.sync` attribute.

    Args:
        class_type: Class with the method to wrap.
        method_name: Name of the asynchronous method to wrap.

    Returns:
        None: Modifies the class method in-place.
    """
    method = getattr(class_type, method_name)

    @functools.wraps(method)
    def syncified(*args, **kwargs):  # type: ignore
        coro = method(*args, **kwargs)
        loop = asyncio.get_event_loop()
        return coro if loop.is_running() else loop.run_until_complete(coro)

    setattr(syncified, "__tl.sync", method)
    setattr(class_type, method_name, syncified)


def syncify(*classes):  # type: ignore
    """Decorate coroutine methods of classes for synchronous execution.

    Iterates over classes, applying `_syncify_wrap` to coroutine methods.
    Enables methods to be used synchronously without managing an asyncio loop.

    Args:
        *classes: Classes to modify for synchronous coroutine method use.
    """
    for c in classes:
        for name in dir(c):
            if (
                not name.startswith("_") or name == "__call__"
            ) and inspect.iscoroutinefunction(getattr(c, name)):
                _syncify_wrap(c, name)  # type: ignore


syncify(  # type: ignore
    Ascii2D,
    BaiDu,
    Bing,
    Copyseeker,
    EHentai,
    Google,
    Iqdb,
    Network,
    SauceNAO,
    Tineye,
    TraceMoe,
    Yandex,
)

__all__ = [
    "Ascii2D",
    "BaiDu",
    "Bing",
    "Copyseeker",
    "EHentai",
    "Google",
    "Iqdb",
    "Network",
    "SauceNAO",
    "Tineye",
    "TraceMoe",
    "Yandex",
]
