from base64 import b64encode
from pathlib import Path

import pytest

from PicImageSearch import AnimeTrace
from tests.conftest import create_engine_image_fixtures

pytestmark = pytest.mark.asyncio
test_image_path, test_image_url = create_engine_image_fixtures("animetrace")


class TestAnimeTrace:
    @pytest.fixture
    def engine(self) -> AnimeTrace:
        return AnimeTrace()

    @pytest.mark.vcr("animetrace_file_search.yaml")
    async def test_search_with_file(self, engine: AnimeTrace, test_image_path: str) -> None:
        result = await engine.search(file=test_image_path)
        assert result.raw
        assert result.raw[0].characters

    @pytest.mark.vcr("animetrace_url_search.yaml")
    async def test_search_with_url(self, engine: AnimeTrace, test_image_url: str) -> None:
        result = await engine.search(url=test_image_url)
        assert result.raw
        assert result.raw[0].characters

    @pytest.mark.vcr("animetrace_base64_search.yaml")
    async def test_search_with_base64(self, engine: AnimeTrace, test_image_path: str) -> None:
        encoded_image = b64encode(Path(test_image_path).read_bytes()).decode()
        result = await engine.search(base64=encoded_image)
        assert result.raw
        assert result.raw[0].characters
