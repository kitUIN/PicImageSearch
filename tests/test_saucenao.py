from typing import Any

import pytest

from PicImageSearch import SauceNAO
from tests.conftest import create_engine_image_fixtures, has_saucenao_config

pytestmark = pytest.mark.asyncio
test_image_path, test_image_url = create_engine_image_fixtures("saucenao")


class TestSauceNAO:
    @pytest.fixture
    def engine(self, test_config: dict[str, Any]) -> SauceNAO:
        if not has_saucenao_config(test_config):
            pytest.skip("Missing SauceNAO configuration")
        return SauceNAO(api_key=test_config["saucenao"]["api_key"])

    @pytest.mark.vcr("saucenao_file_search.yaml")
    async def test_search_with_file(self, engine: SauceNAO, test_image_path: str) -> None:
        result = await engine.search(file=test_image_path)
        assert result.raw

    @pytest.mark.vcr("saucenao_url_search.yaml")
    async def test_search_with_url(self, engine: SauceNAO, test_image_url: str) -> None:
        result = await engine.search(url=test_image_url)
        assert result.raw
