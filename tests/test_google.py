import pytest

from PicImageSearch import Google
from tests.conftest import has_google_config


class TestGoogle:
    @pytest.fixture
    def engine(self, test_config):
        if not has_google_config(test_config):
            pytest.skip("Missing Google configuration")
        return Google(cookies=test_config.get("google", {}).get("cookies"))

    @pytest.fixture
    def test_image_path(self, engine_image_path_mapping):
        return engine_image_path_mapping.get("google")

    @pytest.fixture
    def test_image_url(self, engine_image_url_mapping):
        return engine_image_url_mapping.get("google")

    @pytest.mark.asyncio
    @pytest.mark.vcr("google_file_search.yaml")
    async def test_search_with_file(self, engine, test_image_path):
        result = await engine.search(file=test_image_path)
        assert len(result.raw) > 0

    @pytest.mark.asyncio
    @pytest.mark.vcr("google_url_search.yaml")
    async def test_search_with_url(self, engine, test_image_url):
        result = await engine.search(url=test_image_url)
        assert len(result.raw) > 0
