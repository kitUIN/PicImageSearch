import pytest

from PicImageSearch import Copyseeker, Network


class TestCopyseeker:
    @pytest.fixture
    def test_image_path(self, engine_image_path_mapping):
        return engine_image_path_mapping.get("copyseeker")

    @pytest.fixture
    def test_image_url(self, engine_image_url_mapping):
        return engine_image_url_mapping.get("copyseeker")

    @pytest.mark.asyncio
    @pytest.mark.vcr("copyseeker_file_search.yaml")
    async def test_search_with_file(self, test_image_path):
        async with Network() as client:
            engine = Copyseeker(client=client)
            result = await engine.search(file=test_image_path)
            assert len(result.raw) > 0

    @pytest.mark.asyncio
    @pytest.mark.vcr("copyseeker_url_search.yaml")
    async def test_search_with_url(self, test_image_url):
        async with Network() as client:
            engine = Copyseeker(client=client)
            result = await engine.search(url=test_image_url)
            assert len(result.raw) > 0
