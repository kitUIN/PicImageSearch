import pytest

from PicImageSearch import TraceMoe


class TestTraceMoe:
    @pytest.fixture
    def engine(self):
        return TraceMoe()

    @pytest.fixture
    def test_image_path(self, engine_image_path_mapping):
        return engine_image_path_mapping.get("tracemoe")

    @pytest.fixture
    def test_image_url(self, engine_image_url_mapping):
        return engine_image_url_mapping.get("tracemoe")

    @pytest.mark.asyncio
    @pytest.mark.vcr("tracemoe_file_search.yaml")
    async def test_search_with_file(self, engine, test_image_path):
        result = await engine.search(file=test_image_path)
        assert len(result.raw) > 0

    @pytest.mark.asyncio
    @pytest.mark.vcr("tracemoe_url_search.yaml")
    async def test_search_with_url(self, engine, test_image_url):
        result = await engine.search(url=test_image_url)
        assert len(result.raw) > 0
