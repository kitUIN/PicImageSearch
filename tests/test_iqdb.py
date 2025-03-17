import pytest

from PicImageSearch import Iqdb


class TestIqdb:
    @pytest.fixture
    def engine(self):
        return Iqdb()

    @pytest.fixture
    def test_image(self, get_test_image, engine_image_mapping):
        return get_test_image("iqdb", engine_image_mapping)

    @pytest.mark.asyncio
    async def test_search(self, engine, test_image):
        result = await engine.search(file=test_image)
        assert result is not None
        assert hasattr(result, "raw")
