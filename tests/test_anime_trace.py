from base64 import b64encode
from pathlib import Path

import pytest

from PicImageSearch import AnimeTrace


class TestAnimeTrace:
    @pytest.fixture
    def engine(self):
        return AnimeTrace()

    @pytest.fixture
    def test_image_path(self, engine_image_path_mapping):
        return engine_image_path_mapping.get("animetrace")

    @pytest.fixture
    def test_image_url(self, engine_image_url_mapping):
        return engine_image_url_mapping.get("animetrace")

    @pytest.mark.asyncio
    @pytest.mark.vcr("animetrace_file_search.yaml")
    async def test_search_with_file(self, engine, test_image_path):
        result = await engine.search(file=test_image_path)
        assert len(result.raw) > 0

        item = result.raw[0]
        assert len(item.characters) > 0

    @pytest.mark.asyncio
    @pytest.mark.vcr("animetrace_url_search.yaml")
    async def test_search_with_url(self, engine, test_image_url):
        result = await engine.search(url=test_image_url)
        assert len(result.raw) > 0

        item = result.raw[0]
        assert len(item.characters) > 0

    @pytest.mark.asyncio
    @pytest.mark.vcr("animetrace_base64_search.yaml")
    async def test_search_with_base64(self, engine, test_image_path):
        content = Path(test_image_path).read_bytes()
        base64 = b64encode(content).decode()
        result = await engine.search(base64=base64)
        assert len(result.raw) > 0

        item = result.raw[0]
        assert len(item.characters) > 0
