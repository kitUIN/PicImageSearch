from typing import Any

import pytest

from PicImageSearch import GoogleLens
from tests.conftest import has_google_config


class TestGoogleLens:
    @pytest.fixture
    def engine(self, test_config: dict[str, Any]) -> GoogleLens:
        if not has_google_config(test_config):
            pytest.skip("Missing Google configuration")
        return GoogleLens(cookies=test_config["google"]["cookies"])

    @pytest.fixture
    def test_image_path(self, engine_image_path_mapping: dict[str, str]) -> str:
        return engine_image_path_mapping["googlelens"]

    @pytest.fixture
    def test_image_url(self, engine_image_url_mapping: dict[str, str]) -> str:
        return engine_image_url_mapping["googlelens"]

    @pytest.mark.asyncio
    @pytest.mark.vcr("google_lens_file_search.yaml")
    async def test_search_with_file(self, engine: GoogleLens, test_image_path: str) -> None:
        result = await engine.search(file=test_image_path)
        assert len(result.raw) > 0

    @pytest.mark.asyncio
    @pytest.mark.vcr("google_lens_url_search.yaml")
    async def test_search_with_url(self, engine: GoogleLens, test_image_url: str) -> None:
        result = await engine.search(url=test_image_url)
        assert len(result.raw) > 0
