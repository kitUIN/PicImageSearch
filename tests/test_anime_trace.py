from base64 import b64encode
from pathlib import Path

import pytest

from PicImageSearch import AnimeTrace


class TestAnimeTrace:
    @pytest.fixture
    def engine(self) -> AnimeTrace:
        return AnimeTrace()

    @pytest.fixture
    def test_image_path(self, engine_image_path_mapping: dict[str, str]) -> str:
        return engine_image_path_mapping["animetrace"]

    @pytest.fixture
    def test_image_url(self, engine_image_url_mapping: dict[str, str]) -> str:
        return engine_image_url_mapping["animetrace"]

    @pytest.mark.asyncio
    @pytest.mark.vcr("animetrace_file_search.yaml")
    async def test_search_with_file(self, engine: AnimeTrace, test_image_path: str) -> None:
        result = await engine.search(file=test_image_path)
        assert len(result.raw) > 0

        item = result.raw[0]
        assert len(item.characters) > 0

    @pytest.mark.asyncio
    @pytest.mark.vcr("animetrace_url_search.yaml")
    async def test_search_with_url(self, engine: AnimeTrace, test_image_url: str) -> None:
        result = await engine.search(url=test_image_url)
        assert len(result.raw) > 0

        item = result.raw[0]
        assert len(item.characters) > 0

    @pytest.mark.asyncio
    @pytest.mark.vcr("animetrace_base64_search.yaml")
    async def test_search_with_base64(self, engine: AnimeTrace, test_image_path: str) -> None:
        content = Path(test_image_path).read_bytes()
        base64 = b64encode(content).decode()
        result = await engine.search(base64=base64)
        assert len(result.raw) > 0

        item = result.raw[0]
        assert len(item.characters) > 0
