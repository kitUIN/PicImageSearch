import pytest

from PicImageSearch import Yandex
from tests.conftest import create_engine_image_fixtures

pytestmark = pytest.mark.asyncio
test_image_path, test_image_url = create_engine_image_fixtures("yandex")


class TestYandex:
    @pytest.fixture
    def engine(self) -> Yandex:
        return Yandex()

    @pytest.mark.vcr("yandex_file_search.yaml")
    async def test_search_with_file(self, engine: Yandex, test_image_path: str) -> None:
        result = await engine.search(file=test_image_path)
        assert result.raw

    @pytest.mark.vcr("yandex_url_search.yaml")
    async def test_search_with_url(self, engine: Yandex, test_image_url: str) -> None:
        result = await engine.search(url=test_image_url)
        assert result.raw
