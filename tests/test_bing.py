import pytest

from PicImageSearch import Bing


class TestBing:
    @pytest.fixture
    def engine(self) -> Bing:
        return Bing()

    @pytest.fixture
    def test_image_path(self, engine_image_path_mapping: dict[str, str]) -> str:
        return engine_image_path_mapping["bing"]

    @pytest.fixture
    def test_image_url(self, engine_image_url_mapping: dict[str, str]) -> str:
        return engine_image_url_mapping["bing"]

    @pytest.mark.asyncio
    @pytest.mark.vcr("bing_file_search.yaml")
    async def test_search_with_file(self, engine: Bing, test_image_path: str) -> None:
        result = await engine.search(file=test_image_path)
        assert len(result.visual_search) > 0

    @pytest.mark.asyncio
    @pytest.mark.vcr("bing_url_search.yaml")
    async def test_search_with_url(self, engine: Bing, test_image_url: str) -> None:
        result = await engine.search(url=test_image_url)
        assert len(result.visual_search) > 0
