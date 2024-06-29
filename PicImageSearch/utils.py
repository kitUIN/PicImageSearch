from pathlib import Path
from typing import Union


def read_file(file: Union[str, bytes]) -> bytes:
    """
    Read the file content and return as bytes. If the input is already bytes, return it directly.

    Args:
        file (Union[str, bytes]): The file path or bytes object.

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
