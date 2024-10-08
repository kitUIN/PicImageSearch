import asyncio

from loguru import logger

from src import Network, Yandex
from src.model import YandexResponse
from src.sync import Yandex as YandexSync

proxies = "http://127.0.0.1:1081"
# proxies = None
url = "https://raw.githubusercontent.com/kitUIN/PicImageSearch/main/demo/images/test06.jpg"
file = "../images/test06.jpg"


@logger.catch()
async def test_async() -> None:
    async with Network(proxies=proxies) as client:
        yandex = Yandex(client=client)
        # resp = await yandex.search(url=url)
        resp = await yandex.search(file=file)
        show_result(resp)


@logger.catch()
def test_sync() -> None:
    yandex = YandexSync(proxies=proxies)
    resp = yandex.search(url=url)
    # resp = yandex.search(file=file)
    show_result(resp)  # type: ignore


def show_result(resp: YandexResponse) -> None:
    # logger.info(resp.origin)  # Оригинальные данные
    logger.info(resp.url)  # Ссылка на результаты поиска
    # logger.info(resp.raw[0].origin)
    logger.info(resp.raw[0].title)
    logger.info(resp.raw[0].url)
    logger.info(resp.raw[0].thumbnail)
    logger.info(resp.raw[0].source)
    logger.info(resp.raw[0].content)
    logger.info(resp.raw[0].size)
    logger.info("-" * 50)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_async())
    # test_sync()
