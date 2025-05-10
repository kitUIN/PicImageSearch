"""From: telethon/sync
Rewrites all public asynchronous methods in the library's public interface for synchronous execution.
Useful for scripts, with low runtime overhead. Ideal for synchronous calls preference over managing an event loop.

Automatically wraps asynchronous methods of specified classes, enabling synchronous calls.
"""

import asyncio
import functools
import inspect
from collections.abc import Coroutine
from typing import Any, Callable

from . import (
    AnimeTrace,
    Ascii2D,
    BaiDu,
    Bing,
    Copyseeker,
    EHentai,
    Google,
    GoogleLens,
    Iqdb,
    Lenso,
    Network,
    SauceNAO,
    Tineye,
    TraceMoe,
    Yandex,
)


def _syncify_wrap(class_type: type, method_name: str) -> None:
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
    method: Callable[..., Coroutine[None, None, Any]] = getattr(class_type, method_name)

    @functools.wraps(method)
    def syncified(*args: Any, **kwargs: Any) -> Any:
        coro: Coroutine[None, None, Any] = method(*args, **kwargs)
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return coro if loop.is_running() else loop.run_until_complete(coro)

    setattr(syncified, "__tl.sync", method)
    setattr(class_type, method_name, syncified)


def syncify(*classes: type) -> None:
    """Decorate coroutine methods of classes for synchronous execution.

    Iterates over classes, applying `_syncify_wrap` to coroutine methods.
    Enables methods to be used synchronously without managing an asyncio loop.

    Args:
        *classes: Classes to modify for synchronous coroutine method use.
    """
    for c in classes:
        for name in dir(c):
            attr = getattr(c, name, None)
            if (not name.startswith("_") or name == "__call__") and inspect.iscoroutinefunction(attr):
                _syncify_wrap(c, name)


syncify(
    AnimeTrace,
    Ascii2D,
    BaiDu,
    Bing,
    Copyseeker,
    EHentai,
    Google,
    GoogleLens,
    Iqdb,
    Lenso,
    Network,
    SauceNAO,
    Tineye,
    TraceMoe,
    Yandex,
)

__all__ = [
    "AnimeTrace",
    "Ascii2D",
    "BaiDu",
    "Bing",
    "Copyseeker",
    "EHentai",
    "Google",
    "GoogleLens",
    "Iqdb",
    "Lenso",
    "Network",
    "SauceNAO",
    "Tineye",
    "TraceMoe",
    "Yandex",
]
