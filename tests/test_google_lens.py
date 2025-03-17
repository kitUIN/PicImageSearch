import pytest

from PicImageSearch import GoogleLens
from tests.conftest import has_google_config


class TestGoogleLens:
    @pytest.fixture
    def engine(self, test_config):
        if not has_google_config(test_config):
            pytest.skip("Missing Google configuration")
        return GoogleLens(cookies=test_config.get("google", {}).get("cookies"))

    @pytest.fixture
    def test_image(self, get_test_image, engine_image_mapping):
        return get_test_image("google", engine_image_mapping)

    @pytest.mark.asyncio
    async def test_search(self, engine, test_image):
        result = await engine.search(file=test_image)
        assert result is not None
        assert hasattr(result, "raw")
