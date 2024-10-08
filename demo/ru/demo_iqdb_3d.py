import asyncio

from loguru import logger

from src import Iqdb, Network
from src.model import IqdbResponse
from src.sync import Iqdb as IqdbSync

# proxies = "http://127.0.0.1:1081"
proxies = None
url = "https://raw.githubusercontent.com/kitUIN/PicImageSearch/main/demo/images/test04.jpg"
file = "../images/test04.jpg"


@logger.catch()
async def test_async() -> None:
    async with Network(proxies=proxies) as client:
        iqdb = Iqdb(client=client, is_3d=True)
        # resp = await iqdb.search(url=url)
        resp = await iqdb.search(file=file)
        show_result(resp)


@logger.catch()
def test_sync() -> None:
    iqdb = IqdbSync(proxies=proxies)
    resp = iqdb.search(url=url, is_3d=True)
    # resp = iqdb.search(file=file, is_3d=True)
    show_result(resp)  # type: ignore


def show_result(resp: IqdbResponse) -> None:
    # logger.info(resp.origin)  # Оригинальные данные
    logger.info(resp.url)  # Ссылка на результаты поиска
    # logger.info(resp.raw[0].origin)
    logger.info(f"Описание: {resp.raw[0].content}")
    logger.info(f"URL источника: {resp.raw[0].url}")
    logger.info(f"Миниатюра: {resp.raw[0].thumbnail}")
    logger.info(f"Степень сходства: {resp.raw[0].similarity}")
    logger.info(f"Размер изображения: {resp.raw[0].size}")
    logger.info(f"Источник изображения: {resp.raw[0].source}")
    logger.info(f"Другие источники изображения: {resp.raw[0].other_source}")
    logger.info(
        f"Количество результатов с более низким уровнем сходства: {len(resp.more)}"
    )
    logger.info("-" * 50)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_async())
    # test_sync()
