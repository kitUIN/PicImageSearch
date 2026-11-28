import pytest

from PicImageSearch import Bing, Network
from tests.conftest import create_engine_image_fixtures

pytestmark = pytest.mark.asyncio
test_image_path, test_image_url = create_engine_image_fixtures("bing")


class TestBing:
    @pytest.mark.vcr("bing_file_search.yaml")
    async def test_search_with_file(self, test_image_path: str) -> None:
        async with Network() as client:
            engine = Bing(client=client)
            result = await engine.search(file=test_image_path)
            assert result.visual_search

    @pytest.mark.vcr("bing_url_search.yaml")
    async def test_search_with_url(self, test_image_url: str) -> None:
        async with Network() as client:
            engine = Bing(client=client)
            result = await engine.search(url=test_image_url)
            assert result.visual_search
