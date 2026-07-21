import pytest

from PicImageSearch import BaiDu
from tests.conftest import create_engine_image_fixtures

pytestmark = pytest.mark.asyncio
test_image_path, test_image_url = create_engine_image_fixtures("baidu")


class TestBaiDu:
    @pytest.fixture
    def engine(self) -> BaiDu:
        return BaiDu()

    @pytest.mark.vcr("baidu_file_search.yaml")
    async def test_search_with_file(self, engine: BaiDu, test_image_path: str) -> None:
        result = await engine.search(file=test_image_path)
        assert result.raw

    @pytest.mark.vcr("baidu_url_search.yaml")
    async def test_search_with_url(self, engine: BaiDu, test_image_url: str) -> None:
        result = await engine.search(url=test_image_url)
        assert result.raw
