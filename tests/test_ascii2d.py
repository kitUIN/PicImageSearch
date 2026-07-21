from typing import Any

import pytest

from PicImageSearch import Ascii2D
from tests.conftest import create_engine_image_fixtures, has_ascii2d_config

pytestmark = pytest.mark.asyncio
test_image_path, test_image_url = create_engine_image_fixtures("ascii2d")


class TestAscii2D:
    @pytest.fixture
    def engine(self, test_config: dict[str, Any]) -> Ascii2D:
        if not has_ascii2d_config(test_config):
            pytest.skip("Missing Ascii2D configuration")
        return Ascii2D(base_url=test_config["ascii2d"]["base_url"])

    @pytest.mark.vcr("ascii2d_file_search.yaml")
    async def test_search_with_file(self, engine: Ascii2D, test_image_path: str) -> None:
        result = await engine.search(file=test_image_path)
        assert result.raw

    @pytest.mark.vcr("ascii2d_url_search.yaml")
    async def test_search_with_url(self, engine: Ascii2D, test_image_url: str) -> None:
        result = await engine.search(url=test_image_url)
        assert result.raw
