from typing import Any

import pytest

from PicImageSearch import Google
from tests.conftest import create_engine_image_fixtures, has_google_config

pytestmark = [
    pytest.mark.asyncio,
    pytest.mark.skip(reason="Google engine is deprecated; use GoogleLens instead"),
]
test_image_path, test_image_url = create_engine_image_fixtures("google")


class TestGoogle:
    @pytest.fixture
    def engine(self, test_config: dict[str, Any]) -> Google:
        if not has_google_config(test_config):
            pytest.skip("Missing Google configuration")
        return Google(cookies=test_config["google"]["cookies"])

    @pytest.mark.vcr("google_file_search.yaml")
    async def test_search_with_file(self, engine: Google, test_image_path: str) -> None:
        result = await engine.search(file=test_image_path)
        assert result.raw

    @pytest.mark.vcr("google_url_search.yaml")
    async def test_search_with_url(self, engine: Google, test_image_url: str) -> None:
        result = await engine.search(url=test_image_url)
        assert result.raw
