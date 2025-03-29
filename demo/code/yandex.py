import asyncio

from demo.code.config import IMAGE_BASE_URL, PROXIES, get_image_path, logger
from PicImageSearch import Network, Yandex
from PicImageSearch.model import YandexResponse
from PicImageSearch.sync import Yandex as YandexSync

url = f"{IMAGE_BASE_URL}/test06.jpg"
file = get_image_path("test06.jpg")


@logger.catch()
async def demo_async() -> None:
    async with Network(proxies=PROXIES) as client:
        yandex = Yandex(client=client)
        # resp = await yandex.search(url=url)
        resp = await yandex.search(file=file)
        show_result(resp)


@logger.catch()
def demo_sync() -> None:
    yandex = YandexSync(proxies=PROXIES)
    resp = yandex.search(url=url)
    # resp = yandex.search(file=file)
    show_result(resp)  # pyright: ignore[reportArgumentType]


def show_result(resp: YandexResponse) -> None:
    # logger.info(resp.origin)  # Original data
    logger.info(resp.url)  # Link to search results
    # logger.info(resp.raw[0].origin)
    logger.info(resp.raw[0].title)
    logger.info(resp.raw[0].url)
    logger.info(resp.raw[0].thumbnail)
    logger.info(resp.raw[0].source)
    logger.info(resp.raw[0].content)
    logger.info(resp.raw[0].size)
    logger.info("-" * 50)


if __name__ == "__main__":
    asyncio.run(demo_async())
    # demo_sync()
