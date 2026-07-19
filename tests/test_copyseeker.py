import pytest

from PicImageSearch import Copyseeker, Network


class TestCopyseeker:
    @pytest.fixture
    def test_image_path(self, engine_image_path_mapping: dict[str, str]) -> str:
        return engine_image_path_mapping["copyseeker"]

    @pytest.fixture
    def test_image_url(self, engine_image_url_mapping: dict[str, str]) -> str:
        return engine_image_url_mapping["copyseeker"]

    @pytest.mark.asyncio
    @pytest.mark.vcr("copyseeker_file_search.yaml")
    async def test_search_with_file(self, test_image_path: str) -> None:
        async with Network() as client:
            engine = Copyseeker(client=client)
            result = await engine.search(file=test_image_path)
            assert len(result.raw) > 0

    @pytest.mark.asyncio
    @pytest.mark.vcr("copyseeker_url_search.yaml")
    async def test_search_with_url(self, test_image_url: str) -> None:
        async with Network() as client:
            engine = Copyseeker(client=client)
            result = await engine.search(url=test_image_url)
            assert len(result.raw) > 0
