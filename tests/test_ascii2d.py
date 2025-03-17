import pytest

from PicImageSearch import Ascii2D
from tests.conftest import has_ascii2d_config


class TestAscii2D:
    @pytest.fixture
    def engine(self, test_config):
        if not has_ascii2d_config(test_config):
            pytest.skip("Missing Ascii2D configuration")
        return Ascii2D(base_url=test_config.get("ascii2d", {}).get("base_url"))

    @pytest.fixture
    def test_image(self, get_test_image, engine_image_mapping):
        return get_test_image("ascii2d", engine_image_mapping)

    @pytest.mark.asyncio
    async def test_search(self, engine, test_image):
        result = await engine.search(file=test_image)
        assert result is not None
        assert hasattr(result, "raw")
