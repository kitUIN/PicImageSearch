import sys
from pathlib import Path

from loguru import logger

USE_SIMPLE_LOGGER = False
PROXIES = "http://127.0.0.1:1080"
# PROXIES = None
IMAGE_BASE_URL = "https://raw.githubusercontent.com/kitUIN/PicImageSearch/main/demo/images"
# Note: Google search requires the `NID` cookie (when NOT logged into any Google account), expected format: `NID=...`
GOOGLE_COOKIES = ""

if USE_SIMPLE_LOGGER:
    logger.remove()
    logger.add(sys.stderr, format="<level>{level: <8}</level> <green>{message}</green>")  # pyright: ignore[reportUnusedCallResult]


def get_image_path(image_name: str) -> Path:
    return Path(__file__).parent.parent / "images" / image_name


__all__ = ["GOOGLE_COOKIES", "IMAGE_BASE_URL", "PROXIES", "get_image_path", "logger"]
