import re
from pathlib import Path
from typing import Any, Optional, Union

from lxml.html import HTMLParser, fromstring
from pyquery import PyQuery


def deep_get(dictionary: dict[str, Any], keys: str) -> Optional[Any]:
    """
    Retrieve a value from a nested dictionary using a dot-separated string of keys.

    Args:
        dictionary (dict[str, Any]): The nested dictionary to search in.
        keys (str): The dot-separated string of keys to access.

    Returns:
        Optional[Any]: The value if found, None otherwise.
    """
    for key in keys.split("."):
        if list_search := re.search(r"(\S+)?\[(\d+)]", key):
            try:
                if list_search[1]:
                    dictionary = dictionary[list_search[1]]
                dictionary = dictionary[int(list_search[2])]  # type: ignore
            except (KeyError, IndexError):
                return None
        else:
            try:
                dictionary = dictionary[key]
            except (KeyError, TypeError):
                return None
    return dictionary


def read_file(file: Union[str, bytes, Path]) -> bytes:
    """
    Read the file content and return as bytes. If the input is already bytes, return it directly.

    Args:
        file (Union[str, bytes, Path]): The file path or bytes object.

    Returns:
        bytes: The file content as bytes.

    Raises:
        FileNotFoundError: If the file does not exist.
        IOError: If an I/O error occurs.
    """
    if isinstance(file, bytes):
        return file

    if not Path(file).exists():
        raise FileNotFoundError(f"The file {file} does not exist.")

    try:
        with open(file, "rb") as f:
            return f.read()
    except OSError as e:
        raise OSError(
            f"An I/O error occurred while reading the file {file}: {e}"
        ) from e


def parse_html(html: str) -> PyQuery:
    """Parse HTML content and return a PyQuery object.

    Args:
        html (str): The HTML content to parse.

    Returns:
        PyQuery: A PyQuery object representing the parsed HTML.
    """
    utf8_parser = HTMLParser(encoding="utf-8")
    return PyQuery(fromstring(html, parser=utf8_parser))
