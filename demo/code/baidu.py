import asyncio

from demo.code.config import IMAGE_BASE_URL, get_image_path, logger
from PicImageSearch import BaiDu, Network
from PicImageSearch.model import BaiDuResponse
from PicImageSearch.sync import BaiDu as BaiDuSync

url = f"{IMAGE_BASE_URL}/test02.jpg"
file = get_image_path("test02.jpg")


@logger.catch()
async def demo_async() -> None:
    async with Network() as client:
        baidu = BaiDu(client=client)
        # resp = await baidu.search(url=url)
        resp = await baidu.search(file=file)
        show_result(resp)


@logger.catch()
def demo_sync() -> None:
    baidu = BaiDuSync()
    resp = baidu.search(url=url)
    # resp = baidu.search(file=file)
    show_result(resp)  # pyright: ignore[reportArgumentType]


def show_result(resp: BaiDuResponse) -> None:
    # logger.info(resp.origin)  # Original data
    logger.info(resp.url)  # Link to search results
    result = resp.raw[0]
    # logger.info(result.origin)
    # logger.info(result.similarity)  # deprecated
    logger.info(result.url)
    logger.info(result.thumbnail)

    if resp.exact_matches:
        exact_match = resp.exact_matches[0]
        logger.info("-" * 20)
        logger.info(exact_match.title)
        logger.info(exact_match.url)
        logger.info(exact_match.thumbnail)

    logger.info("-" * 50)


if __name__ == "__main__":
    asyncio.run(demo_async())
    # demo_sync()
