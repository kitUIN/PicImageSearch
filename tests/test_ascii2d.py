import pytest

from PicImageSearch import Ascii2D
from tests.conftest import has_ascii2d_config


class TestAscii2D:
    @pytest.fixture
    def engine(self, test_config):
        if not has_ascii2d_config(test_config):
            pytest.skip("Missing Ascii2D configuration")
        return Ascii2D(base_url=test_config.get("ascii2d", {}).get("base_url"))

    @pytest.fixture
    def test_image_path(self, engine_image_path_mapping):
        return engine_image_path_mapping.get("ascii2d")

    @pytest.fixture
    def test_image_url(self, engine_image_url_mapping):
        return engine_image_url_mapping.get("ascii2d")

    @pytest.mark.asyncio
    @pytest.mark.vcr("ascii2d_file_search.yaml")
    async def test_search_with_file(self, engine, test_image_path):
        result = await engine.search(file=test_image_path)
        assert len(result.raw) > 0

    @pytest.mark.asyncio
    @pytest.mark.vcr("ascii2d_url_search.yaml")
    async def test_search_with_url(self, engine, test_image_url):
        result = await engine.search(url=test_image_url)
        assert len(result.raw) > 0
