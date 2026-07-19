from typing import Any

import pytest

from PicImageSearch import Ascii2D
from tests.conftest import has_ascii2d_config


class TestAscii2D:
    @pytest.fixture
    def engine(self, test_config: dict[str, Any]) -> Ascii2D:
        if not has_ascii2d_config(test_config):
            pytest.skip("Missing Ascii2D configuration")
        return Ascii2D(base_url=test_config.get("ascii2d", {}).get("base_url"))

    @pytest.fixture
    def test_image_path(self, engine_image_path_mapping: dict[str, str]) -> str:
        return engine_image_path_mapping["ascii2d"]

    @pytest.fixture
    def test_image_url(self, engine_image_url_mapping: dict[str, str]) -> str:
        return engine_image_url_mapping["ascii2d"]

    @pytest.mark.asyncio
    @pytest.mark.vcr("ascii2d_file_search.yaml")
    async def test_search_with_file(self, engine: Ascii2D, test_image_path: str) -> None:
        result = await engine.search(file=test_image_path)
        assert len(result.raw) > 0

    @pytest.mark.asyncio
    @pytest.mark.vcr("ascii2d_url_search.yaml")
    async def test_search_with_url(self, engine: Ascii2D, test_image_url: str) -> None:
        result = await engine.search(url=test_image_url)
        assert len(result.raw) > 0
