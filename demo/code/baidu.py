import asyncio

from demo.code.config import IMAGE_BASE_URL, PROXIES, get_image_path, logger
from PicImageSearch import BaiDu, Network
from PicImageSearch.model import BaiDuResponse
from PicImageSearch.sync import BaiDu as BaiDuSync

url = f"{IMAGE_BASE_URL}/test02.jpg"
file = get_image_path("test02.jpg")


@logger.catch()
async def test_async() -> None:
    async with Network(proxies=PROXIES) as client:
        baidu = BaiDu(client=client)
        # resp = await baidu.search(url=url)
        resp = await baidu.search(file=file)
        show_result(resp)


@logger.catch()
def test_sync() -> None:
    baidu = BaiDuSync(proxies=PROXIES)
    resp = baidu.search(url=url)
    # resp = baidu.search(file=file)
    show_result(resp)  # type: ignore


def show_result(resp: BaiDuResponse) -> None:
    # logger.info(resp.origin)  # Original data
    logger.info(resp.url)  # Link to search results
    # logger.info(resp.raw[0].origin)
    # logger.info(resp.raw[0].similarity)  # deprecated
    # logger.info(resp.raw[0].title)  # deprecated
    logger.info(resp.raw[0].url)
    logger.info(resp.raw[0].thumbnail)
    logger.info("-" * 50)


if __name__ == "__main__":
    asyncio.run(test_async())  # type: ignore
    # test_sync()  # type: ignore
