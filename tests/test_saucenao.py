from typing import Any

import pytest

from PicImageSearch import SauceNAO
from tests.conftest import has_saucenao_config


class TestSauceNAO:
    @pytest.fixture
    def engine(self, test_config: dict[str, Any]) -> SauceNAO:
        if not has_saucenao_config(test_config):
            pytest.skip("Missing SauceNAO configuration")
        return SauceNAO(api_key=test_config.get("saucenao", {}).get("api_key"))

    @pytest.fixture
    def test_image_path(self, engine_image_path_mapping: dict[str, str]) -> str:
        return engine_image_path_mapping["saucenao"]

    @pytest.fixture
    def test_image_url(self, engine_image_url_mapping: dict[str, str]) -> str:
        return engine_image_url_mapping["saucenao"]

    @pytest.mark.asyncio
    @pytest.mark.vcr("saucenao_file_search.yaml")
    async def test_search_with_file(self, engine: SauceNAO, test_image_path: str) -> None:
        result = await engine.search(file=test_image_path)
        assert len(result.raw) > 0

    @pytest.mark.asyncio
    @pytest.mark.vcr("saucenao_url_search.yaml")
    async def test_search_with_url(self, engine: SauceNAO, test_image_url: str) -> None:
        result = await engine.search(url=test_image_url)
        assert len(result.raw) > 0
