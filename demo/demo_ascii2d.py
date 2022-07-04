import asyncio

from loguru import logger

from PicImageSearch import Ascii2D, Network
from PicImageSearch.model import Ascii2DResponse
from PicImageSearch.sync import Ascii2D as Ascii2DSync

# proxies = "http://127.0.0.1:1081"
proxies = None
url = "https://raw.githubusercontent.com/kitUIN/PicImageSearch/main/demo/images/test01.jpg"
file = open(r"images/test01.jpg", "rb")
bovw = True  # 是否使用特征检索
bypass = False  # 是否绕过DNS污染


@logger.catch()
async def test() -> None:
    async with Network(proxies=proxies) as client:
        ascii2d = Ascii2D(client=client, bovw=bovw, bypass=bypass)
        # resp = await ascii2d.search(url=url)
        resp = await ascii2d.search(file=file)
        show_result(resp)


@logger.catch()
def test_sync() -> None:
    ascii2d = Ascii2DSync(proxies=proxies, bovw=bovw, bypass=bypass)
    resp = ascii2d.search(url=url)
    # resp = ascii2d.search(file=file)
    show_result(resp)  # type: ignore


def show_result(resp: Ascii2DResponse) -> None:
    # logger.info(resp.origin)  # 原始数据
    logger.info(resp.url)  # 搜索结果链接
    logger.info(resp.raw[1].origin)
    logger.info(resp.raw[1].thumbnail)
    logger.info(resp.raw[1].title)
    logger.info(resp.raw[1].author)
    logger.info(resp.raw[1].author_url)
    logger.info(resp.raw[1].url)
    logger.info(resp.raw[1].hash)
    logger.info(resp.raw[1].detail)
    logger.info(resp.raw[1].mark)
    logger.info("-" * 50)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
    # test_sync()
