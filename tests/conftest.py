import os
from typing import Any

import pytest


def pytest_configure(config):
    """Configure test environment"""
    # Create test configuration directory
    os.makedirs("tests/config", exist_ok=True)


def pytest_addoption(parser):
    """Add command line options"""
    parser.addoption(
        "--test-config-file",
        action="store",
        default="tests/config/test_config.json",
        help="Test configuration file path",
    )


@pytest.fixture(scope="session")
def test_config(request) -> dict[str, Any]:
    """Load test configuration"""
    import json

    config_file = request.config.getoption("--test-config-file")

    if os.path.exists(config_file):
        with open(config_file, encoding="utf-8") as f:
            return json.load(f)
    return {}


@pytest.fixture(scope="session")
def test_image_path() -> str:
    """Test image path"""
    return "demo/images/test01.jpg"


# Add an image mapping dictionary to specify different test images for different engines
@pytest.fixture(scope="session")
def engine_image_mapping() -> dict[str, str]:
    """Map engine names to corresponding test image paths"""
    return {
        "animetrace": "demo/images/test05.jpg",
        "ascii2d": "demo/images/test01.jpg",
        "baidu": "demo/images/test02.jpg",
        "bing": "demo/images/test08.jpg",
        "copyseeker": "demo/images/test05.jpg",
        "ehentai": "demo/images/test06.jpg",
        "google": "demo/images/test03.jpg",
        "googlelens": "demo/images/test05.jpg",
        "iqdb": "demo/images/test01.jpg",
        "lenso": "demo/images/test08.jpg",
        "saucenao": "demo/images/test01.jpg",
        "tineye": "demo/images/test07.jpg",
        "tracemoe": "demo/images/test05.jpg",
        "yandex": "demo/images/test06.jpg",
    }


@pytest.fixture
def get_test_image():
    """Factory function to get test image data for specified engine"""

    def _get_image(engine_name: str, mapping: dict[str, str]):
        image_path = mapping.get(engine_name.lower(), "demo/images/test01.jpg")
        try:
            with open(image_path, "rb") as f:
                return f.read()
        except FileNotFoundError:
            pytest.skip(f"Test image {image_path} does not exist")

    return _get_image


# Configuration check functions for each engine
def has_ascii2d_config(config: dict[str, Any]) -> bool:
    return bool(config.get("ascii2d", {}).get("base_url"))


def has_baidu_config(config: dict[str, Any]) -> bool:
    return bool(config.get("baidu", {}).get("cookies"))


def has_google_config(config: dict[str, Any]) -> bool:
    return bool(config.get("google", {}).get("cookies"))


def has_saucenao_config(config: dict[str, Any]) -> bool:
    return bool(config.get("saucenao", {}).get("api_key"))
