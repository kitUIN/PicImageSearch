import pytest

from PicImageSearch import Tineye


class TestTineye:
    @pytest.fixture
    def engine(self) -> Tineye:
        return Tineye()

    @pytest.fixture
    def test_image_path(self, engine_image_path_mapping: dict[str, str]) -> str:
        return engine_image_path_mapping["tineye"]

    @pytest.fixture
    def test_image_url(self, engine_image_url_mapping: dict[str, str]) -> str:
        return engine_image_url_mapping["tineye"]

    @pytest.mark.asyncio
    @pytest.mark.vcr("tineye_file_search.yaml")
    async def test_search_with_file(self, engine: Tineye, test_image_path: str) -> None:
        result = await engine.search(file=test_image_path)
        assert len(result.raw) > 0

    @pytest.mark.asyncio
    @pytest.mark.vcr("tineye_url_search.yaml")
    async def test_search_with_url(self, engine: Tineye, test_image_url: str) -> None:
        result = await engine.search(url=test_image_url)
        assert len(result.raw) > 0
