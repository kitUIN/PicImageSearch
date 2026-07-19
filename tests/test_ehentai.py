import pytest

from PicImageSearch import EHentai


class TestEHentai:
    @pytest.fixture
    def engine(self) -> EHentai:
        return EHentai()

    @pytest.fixture
    def test_image_path(self, engine_image_path_mapping: dict[str, str]) -> str:
        return engine_image_path_mapping["ehentai"]

    @pytest.fixture
    def test_image_url(self, engine_image_url_mapping: dict[str, str]) -> str:
        return engine_image_url_mapping["ehentai"]

    @pytest.mark.asyncio
    @pytest.mark.vcr("ehentai_file_search.yaml")
    async def test_search_with_file(self, engine: EHentai, test_image_path: str) -> None:
        result = await engine.search(file=test_image_path)
        assert len(result.raw) > 0

    @pytest.mark.asyncio
    @pytest.mark.vcr("ehentai_url_search.yaml")
    async def test_search_with_url(self, engine: EHentai, test_image_url: str) -> None:
        result = await engine.search(url=test_image_url)
        assert len(result.raw) > 0
