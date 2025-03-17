import pytest

from PicImageSearch import SauceNAO
from tests.conftest import has_saucenao_config


class TestSauceNAO:
    @pytest.fixture
    def engine(self, test_config):
        if not has_saucenao_config(test_config):
            pytest.skip("Missing SauceNAO configuration")
        return SauceNAO(api_key=test_config.get("saucenao", {}).get("api_key"))

    @pytest.fixture
    def test_image(self, get_test_image, engine_image_mapping):
        return get_test_image("saucenao", engine_image_mapping)

    @pytest.mark.asyncio
    async def test_search(self, engine, test_image):
        result = await engine.search(file=test_image)
        assert result is not None
        assert hasattr(result, "raw")
