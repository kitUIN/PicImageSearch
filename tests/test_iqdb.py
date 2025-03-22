import pytest

from PicImageSearch import Iqdb


class TestIqdb:
    @pytest.fixture
    def engine(self):
        return Iqdb()

    @pytest.fixture
    def test_image_path(self, engine_image_path_mapping):
        return engine_image_path_mapping.get("iqdb")

    @pytest.fixture
    def test_image_url(self, engine_image_url_mapping):
        return engine_image_url_mapping.get("iqdb")

    @pytest.mark.asyncio
    @pytest.mark.vcr("iqdb_file_search.yaml")
    async def test_search_with_file(self, engine, test_image_path):
        result = await engine.search(file=test_image_path)
        assert len(result.raw) > 0

    @pytest.mark.asyncio
    @pytest.mark.vcr("iqdb_url_search.yaml")
    async def test_search_with_url(self, engine, test_image_url):
        result = await engine.search(url=test_image_url)
        assert len(result.raw) > 0
