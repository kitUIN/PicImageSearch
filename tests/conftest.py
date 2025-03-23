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
@pytest.fixture(scope="session")
def engine_image_path_mapping() -> dict[str, str]:
    """Map engine names to corresponding test image paths"""
    base_path = "demo/images"
    return {
        "animetrace": f"{base_path}/test05.jpg",
        "ascii2d": f"{base_path}/test01.jpg",
        "baidu": f"{base_path}/test02.jpg",
        "bing": f"{base_path}/test08.jpg",
        "copyseeker": f"{base_path}/test05.jpg",
        "ehentai": f"{base_path}/test06.jpg",
        "google": f"{base_path}/test03.jpg",
        "googlelens": f"{base_path}/test05.jpg",
        "iqdb": f"{base_path}/test01.jpg",
        "saucenao": f"{base_path}/test01.jpg",
        "tineye": f"{base_path}/test07.jpg",
        "tracemoe": f"{base_path}/test05.jpg",
        "yandex": f"{base_path}/test06.jpg",
    }


@pytest.fixture(scope="session")
def engine_image_url_mapping() -> dict[str, str]:
    """Map engine names to corresponding test image URLs"""
    base_url = "https://raw.githubusercontent.com/kitUIN/PicImageSearch/main/demo/images"
    return {
        "animetrace": f"{base_url}/test05.jpg",
        "ascii2d": f"{base_url}/test01.jpg",
        "baidu": f"{base_url}/test02.jpg",
        "bing": f"{base_url}/test08.jpg",
        "copyseeker": f"{base_url}/test05.jpg",
        "ehentai": f"{base_url}/test06.jpg",
        "google": f"{base_url}/test03.jpg",
        "googlelens": f"{base_url}/test05.jpg",
        "iqdb": f"{base_url}/test01.jpg",
        "saucenao": f"{base_url}/test01.jpg",
        "tineye": f"{base_url}/test07.jpg",
        "tracemoe": f"{base_url}/test05.jpg",
        "yandex": f"{base_url}/test06.jpg",
    }


# Configuration check functions for each engine
def has_ascii2d_config(config: dict[str, Any]) -> bool:
    return bool(config.get("ascii2d", {}).get("base_url"))


def has_google_config(config: dict[str, Any]) -> bool:
    return bool(config.get("google", {}).get("cookies"))


def has_saucenao_config(config: dict[str, Any]) -> bool:
    return bool(config.get("saucenao", {}).get("api_key"))
