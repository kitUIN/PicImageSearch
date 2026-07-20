import os
from typing import Any

import pytest


def pytest_configure(config):
    """Configure test environment"""
    # Create test configuration directory
    os.makedirs("tests/config", exist_ok=True)
    # Create vcr cassettes directory
    os.makedirs("tests/cassettes", exist_ok=True)

    # Import modules required by vcr
    import vcr.stubs.httpx_stubs
    from vcr.request import Request as VcrRequest

    # Add monkey patch to fix VCR handling of binary requests
    def patched_make_vcr_request(httpx_request, **kwargs):
        # Use binary data directly, don't attempt UTF-8 decoding
        body = httpx_request.read()
        uri = str(httpx_request.url)
        headers = dict(httpx_request.headers)
        return VcrRequest(httpx_request.method, uri, body, headers)

    # Apply monkey patch
    vcr.stubs.httpx_stubs._make_vcr_request = patched_make_vcr_request


def pytest_addoption(parser):
    """Add command line options"""
    parser.addoption(
        "--test-config-file",
        action="store",
        default="tests/config/test_config.json",
        help="Test configuration file path",
    )


# VCR related configuration
@pytest.fixture(scope="module", autouse=True)
def vcr_config():
    """Configure pytest-vcr"""
    return {
        # cassette file storage location
        "cassette_library_dir": "tests/cassettes",
        # mode setting
        "record_mode": "once",
    }


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
_ENGINE_IMAGE_FILENAMES = {
    "animetrace": "test05.jpg",
    "ascii2d": "test01.jpg",
    "baidu": "test02.jpg",
    "bing": "test08.jpg",
    "copyseeker": "test05.jpg",
    "ehentai": "test06.jpg",
    "google": "test03.jpg",
    "googlelens": "test05.jpg",
    "iqdb": "test01.jpg",
    "saucenao": "test01.jpg",
    "tineye": "test07.jpg",
    "tracemoe": "test05.jpg",
    "yandex": "test06.jpg",
}


@pytest.fixture(scope="session")
def engine_image_path_mapping() -> dict[str, str]:
    """Map engine names to corresponding test image paths"""
    base_path = "demo/images"
    return {engine: f"{base_path}/{filename}" for engine, filename in _ENGINE_IMAGE_FILENAMES.items()}


@pytest.fixture(scope="session")
def engine_image_url_mapping() -> dict[str, str]:
    """Map engine names to corresponding test image URLs"""
    base_url = "https://raw.githubusercontent.com/kitUIN/PicImageSearch/main/demo/images"
    return {engine: f"{base_url}/{filename}" for engine, filename in _ENGINE_IMAGE_FILENAMES.items()}


# Configuration check functions for each engine
def has_ascii2d_config(config: dict[str, Any]) -> bool:
    return bool(config.get("ascii2d", {}).get("base_url"))


def has_google_config(config: dict[str, Any]) -> bool:
    return bool(config.get("google", {}).get("cookies"))


def has_saucenao_config(config: dict[str, Any]) -> bool:
    return bool(config.get("saucenao", {}).get("api_key"))
