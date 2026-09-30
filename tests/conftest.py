import json
from pathlib import Path
from typing import Any, cast

import pytest


def pytest_configure(config: pytest.Config) -> None:
    tests_directory = config.invocation_params.dir / "tests"
    for directory in ("config", "cassettes"):
        (tests_directory / directory).mkdir(parents=True, exist_ok=True)


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--test-config-file",
        action="store",
        default="tests/config/test_config.json",
        help="Test configuration file path",
    )


@pytest.fixture(scope="module", autouse=True)
def vcr_config() -> dict[str, str]:
    return {
        "cassette_library_dir": "tests/cassettes",
        "record_mode": "once",
    }


@pytest.fixture(scope="session")
def test_config(request: pytest.FixtureRequest) -> dict[str, Any]:
    config_path = Path(cast(str, request.config.getoption("--test-config-file")))
    if not config_path.exists():
        return {}

    with config_path.open(encoding="utf-8") as config_file:
        return json.load(config_file)


@pytest.fixture(scope="session")
def test_image_path() -> str:
    return "demo/images/test01.jpg"


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


def _build_engine_image_mapping(base: str) -> dict[str, str]:
    return {engine: f"{base}/{filename}" for engine, filename in _ENGINE_IMAGE_FILENAMES.items()}


@pytest.fixture(scope="session")
def engine_image_path_mapping() -> dict[str, str]:
    return _build_engine_image_mapping("demo/images")


@pytest.fixture(scope="session")
def engine_image_url_mapping() -> dict[str, str]:
    return _build_engine_image_mapping("https://raw.githubusercontent.com/kitUIN/PicImageSearch/main/demo/images")


def create_engine_image_fixtures(engine_name: str):
    @pytest.fixture
    def test_image_path(engine_image_path_mapping: dict[str, str]) -> str:
        return engine_image_path_mapping[engine_name]

    @pytest.fixture
    def test_image_url(engine_image_url_mapping: dict[str, str]) -> str:
        return engine_image_url_mapping[engine_name]

    return test_image_path, test_image_url


def has_ascii2d_config(config: dict[str, Any]) -> bool:
    return bool(config.get("ascii2d", {}).get("base_url"))


def has_google_config(config: dict[str, Any]) -> bool:
    return bool(config.get("google", {}).get("cookies"))


def has_saucenao_config(config: dict[str, Any]) -> bool:
    return bool(config.get("saucenao", {}).get("api_key"))
