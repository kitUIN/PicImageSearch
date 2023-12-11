import asyncio

from loguru import logger

from PicImageSearch import BaiDu, Network
from PicImageSearch.model import BaiDuResponse
from PicImageSearch.sync import BaiDu as BaiDuSync

# proxies = "http://127.0.0.1:1081"
proxies = None
url = "https://raw.githubusercontent.com/kitUIN/PicImageSearch/main/demo/images/test02.jpg"
file = "images/test02.jpg"


@logger.catch()
async def test_async() -> None:
    async with Network(proxies=proxies) as client:
        baidu = BaiDu(client=client)
        # resp = await baidu.search(url=url)
        resp = await baidu.search(file=file)
        show_result(resp)


@logger.catch()
def test_sync() -> None:
    baidu = BaiDuSync(proxies=proxies)
    resp = baidu.search(url=url)
    # resp = baidu.search(file=file)
    show_result(resp)  # type: ignore


def show_result(resp: BaiDuResponse) -> None:
    # logger.info(resp.origin)  # 原始数据
    logger.info(resp.url)
    # logger.info(resp.raw[0].origin)
    # logger.info(resp.raw[0].similarity)  # deprecated
    # logger.info(resp.raw[0].title)  # deprecated
    logger.info(resp.raw[0].url)
    logger.info(resp.raw[0].thumbnail)
    logger.info("-" * 50)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_async())
    # test_sync()
