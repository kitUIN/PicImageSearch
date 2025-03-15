import re
from pathlib import Path
from typing import Any, Optional, Union

from lxml.html import HTMLParser, fromstring
from pyquery import PyQuery


def deep_get(dictionary: dict[str, Any], keys: str) -> Optional[Any]:
    """Retrieves a value from a nested dictionary using a dot-separated string of keys.

    This function supports both dictionary key access and list index access:
    - Simple key: 'key1.key2'
    - List index: 'key1[0]'
    - Combined: 'key1[0].key2'

    Args:
        dictionary (dict[str, Any]): The nested dictionary to search in.
        keys (str): A dot-separated string of keys, which can include list indices in square brackets.

    Returns:
        The value if found, None if any key in the path doesn't exist or if the path is invalid.

    Examples:
        >>> data = {'a': {'b': [{'c': 1}]}}
        >>> deep_get(data, 'a.b[0].c')
        1
        >>> deep_get(data, 'a.b[1]')
        None
    """
    for key in keys.split("."):
        if list_search := re.search(r"(\S+)?\[(\d+)]", key):
            try:
                if list_search[1]:
                    dictionary = dictionary[list_search[1]]
                dictionary = dictionary[int(list_search[2])]  # pyright: ignore[reportArgumentType]
            except (KeyError, IndexError):
                return None
        else:
            try:
                dictionary = dictionary[key]
            except (KeyError, TypeError):
                return None
    return dictionary


def read_file(file: Union[str, bytes, Path]) -> bytes:
    """Reads file content and returns it as bytes.

    This function handles different input types:
    - Path-like objects (str or Path)
    - Bytes data (returns directly)

    Args:
        file (Union[str, bytes, Path]): The input to read from. Can be:
            - A string path to the file
            - A Path object
            - Bytes data

    Returns:
        The file content as bytes.

    Raises:
        FileNotFoundError: If the specified file path doesn't exist.
        OSError: If any I/O related errors occur during file reading.

    Note:
        If the input is already bytes, it will be returned without modification.
    """
    if isinstance(file, bytes):
        return file

    if not Path(file).exists():
        raise FileNotFoundError(f"The file {file} does not exist.")

    try:
        with open(file, "rb") as f:
            return f.read()
    except OSError as e:
        raise OSError(f"An I/O error occurred while reading the file {file}: {e}") from e


def parse_html(html: str) -> PyQuery:
    """Parses HTML content into a PyQuery object using UTF-8 encoding.

    This function creates a PyQuery object from HTML string content,
    ensuring proper UTF-8 encoding during parsing.

    Args:
        html (str): The HTML content to parse as a string.

    Returns:
        A PyQuery object representing the parsed HTML document.

    Note:
        Uses lxml's HTMLParser with explicit UTF-8 encoding to prevent
        potential character encoding issues.
    """
    utf8_parser = HTMLParser(encoding="utf-8")
    return PyQuery(fromstring(html, parser=utf8_parser))
