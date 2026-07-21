from typing import Any

import pytest

from PicImageSearch import GoogleLens
from tests.conftest import create_engine_image_fixtures, has_google_config

pytestmark = pytest.mark.asyncio
test_image_path, test_image_url = create_engine_image_fixtures("googlelens")


class TestGoogleLens:
    @pytest.fixture
    def engine(self, test_config: dict[str, Any]) -> GoogleLens:
        if not has_google_config(test_config):
            pytest.skip("Missing Google configuration")
        return GoogleLens(cookies=test_config["google"]["cookies"])

    @pytest.mark.vcr("google_lens_file_search.yaml")
    async def test_search_with_file(self, engine: GoogleLens, test_image_path: str) -> None:
        result = await engine.search(file=test_image_path)
        assert result.raw

    @pytest.mark.vcr("google_lens_url_search.yaml")
    async def test_search_with_url(self, engine: GoogleLens, test_image_url: str) -> None:
        result = await engine.search(url=test_image_url)
        assert result.raw
