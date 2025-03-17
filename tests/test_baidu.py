import pytest

from PicImageSearch import BaiDu
from tests.conftest import has_baidu_config


class TestBaiDu:
    @pytest.fixture
    def engine(self, test_config):
        if not has_baidu_config(test_config):
            pytest.skip("Missing BaiDu configuration")
        return BaiDu(cookies=test_config.get("baidu", {}).get("cookies"))

    @pytest.fixture
    def test_image(self, get_test_image, engine_image_mapping):
        return get_test_image("baidu", engine_image_mapping)

    @pytest.mark.asyncio
    async def test_search(self, engine, test_image):
        result = await engine.search(file=test_image)
        assert result is not None
        assert hasattr(result, "raw")
