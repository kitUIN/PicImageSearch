import pytest

from PicImageSearch import Tineye
from tests.conftest import create_engine_image_fixtures

pytestmark = pytest.mark.asyncio
test_image_path, test_image_url = create_engine_image_fixtures("tineye")


class TestTineye:
    @pytest.fixture
    def engine(self) -> Tineye:
        return Tineye()

    @pytest.mark.vcr("tineye_file_search.yaml")
    async def test_search_with_file(self, engine: Tineye, test_image_path: str) -> None:
        result = await engine.search(file=test_image_path)
        assert result.raw

    @pytest.mark.vcr("tineye_url_search.yaml")
    async def test_search_with_url(self, engine: Tineye, test_image_url: str) -> None:
        result = await engine.search(url=test_image_url)
        assert result.raw
