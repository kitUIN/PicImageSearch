import sys
from pathlib import Path

from loguru import logger

USE_SIMPLE_LOGGER = True
PROXIES = "http://127.0.0.1:1080"
# PROXIES = None
IMAGE_BASE_URL = (
    "https://raw.githubusercontent.com/kitUIN/PicImageSearch/main/demo/images"
)

if USE_SIMPLE_LOGGER:
    logger.remove()
    logger.add(sys.stderr, format="<level>{level: <8}</level> <green>{message}</green>")


def get_image_path(image_name: str) -> Path:
    return Path(__file__).parent.parent / "images" / image_name


__all__ = ["IMAGE_BASE_URL", "PROXIES", "get_image_path", "logger"]
