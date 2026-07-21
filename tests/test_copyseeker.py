import pytest

from PicImageSearch import Copyseeker, Network
from tests.conftest import create_engine_image_fixtures

pytestmark = pytest.mark.asyncio
test_image_path, test_image_url = create_engine_image_fixtures("copyseeker")


class TestCopyseeker:
    @pytest.mark.vcr("copyseeker_file_search.yaml")
    async def test_search_with_file(self, test_image_path: str) -> None:
        async with Network() as client:
            engine = Copyseeker(client=client)
            result = await engine.search(file=test_image_path)
            assert result.raw

    @pytest.mark.vcr("copyseeker_url_search.yaml")
    async def test_search_with_url(self, test_image_url: str) -> None:
        async with Network() as client:
            engine = Copyseeker(client=client)
            result = await engine.search(url=test_image_url)
            assert result.raw
