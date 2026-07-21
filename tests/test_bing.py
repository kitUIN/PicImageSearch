import pytest

from PicImageSearch import Bing
from tests.conftest import create_engine_image_fixtures

pytestmark = pytest.mark.asyncio
test_image_path, test_image_url = create_engine_image_fixtures("bing")


class TestBing:
    @pytest.fixture
    def engine(self) -> Bing:
        return Bing()

    @pytest.mark.vcr("bing_file_search.yaml")
    async def test_search_with_file(self, engine: Bing, test_image_path: str) -> None:
        result = await engine.search(file=test_image_path)
        assert result.visual_search

    @pytest.mark.vcr("bing_url_search.yaml")
    async def test_search_with_url(self, engine: Bing, test_image_url: str) -> None:
        result = await engine.search(url=test_image_url)
        assert result.visual_search
