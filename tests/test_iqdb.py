import pytest

from PicImageSearch import Iqdb


class TestIqdb:
    @pytest.fixture
    def engine(self) -> Iqdb:
        return Iqdb()

    @pytest.fixture
    def test_image_path(self, engine_image_path_mapping: dict[str, str]) -> str:
        return engine_image_path_mapping["iqdb"]

    @pytest.fixture
    def test_image_url(self, engine_image_url_mapping: dict[str, str]) -> str:
        return engine_image_url_mapping["iqdb"]

    @pytest.mark.asyncio
    @pytest.mark.vcr("iqdb_file_search.yaml")
    async def test_search_with_file(self, engine: Iqdb, test_image_path: str) -> None:
        result = await engine.search(file=test_image_path)
        assert len(result.raw) > 0

    @pytest.mark.asyncio
    @pytest.mark.vcr("iqdb_url_search.yaml")
    async def test_search_with_url(self, engine: Iqdb, test_image_url: str) -> None:
        result = await engine.search(url=test_image_url)
        assert len(result.raw) > 0
