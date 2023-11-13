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

from . import Ascii2D, BaiDu, EHentai, Google, Iqdb, Network, SauceNAO, TraceMoe, Yandex


def _syncify_wrap(t, method_name):  # type: ignore
    """Wrap an asynchronous method to allow synchronous execution.

    The wrapper checks if the event loop is already running, and executes the method
    accordingly. The original asynchronous method is stored as `__tl.sync` attribute.

    Args:
        class_type: The class containing the method to wrap.
        method_name: The name of the method to wrap.

    Returns:
        A wrapped synchronous method which can be called directly.
    """
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
    """Decorate all coroutine methods of given classes to enable synchronous calling.

    This function applies `_syncify_wrap` decorator to all coroutine methods
    of the passed in classes, allowing those methods to be run synchronously.

    Args:
        classes: A variable number of class objects to syncify.
    """
    for t in types:
        for name in dir(t):
            if (
                not name.startswith("_") or name == "__call__"
            ) and inspect.iscoroutinefunction(getattr(t, name)):
                _syncify_wrap(t, name)  # type: ignore


syncify(Ascii2D, BaiDu, EHentai, Google, Iqdb, Network, SauceNAO, TraceMoe, Yandex)  # type: ignore

__all__ = [
    "Ascii2D",
    "BaiDu",
    "EHentai",
    "Google",
    "Iqdb",
    "Network",
    "SauceNAO",
    "TraceMoe",
    "Yandex",
]
