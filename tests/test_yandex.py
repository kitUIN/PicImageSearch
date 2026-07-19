import pytest

from PicImageSearch import Yandex


class TestYandex:
    @pytest.fixture
    def engine(self) -> Yandex:
        return Yandex()

    @pytest.fixture
    def test_image_path(self, engine_image_path_mapping: dict[str, str]) -> str:
        return engine_image_path_mapping["yandex"]

    @pytest.fixture
    def test_image_url(self, engine_image_url_mapping: dict[str, str]) -> str:
        return engine_image_url_mapping["yandex"]

    @pytest.mark.asyncio
    @pytest.mark.vcr("yandex_file_search.yaml")
    async def test_search_with_file(self, engine: Yandex, test_image_path: str) -> None:
        result = await engine.search(file=test_image_path)
        assert len(result.raw) > 0

    @pytest.mark.asyncio
    @pytest.mark.vcr("yandex_url_search.yaml")
    async def test_search_with_url(self, engine: Yandex, test_image_url: str) -> None:
        result = await engine.search(url=test_image_url)
        assert len(result.raw) > 0
