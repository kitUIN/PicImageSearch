import asyncio

from loguru import logger

from PicImageSearch import BaiDu, Network
from PicImageSearch.model import BaiDuResponse
from PicImageSearch.sync import BaiDu as BaiDuSync

# proxies = "http://127.0.0.1:1081"
proxies = None
url = "https://raw.githubusercontent.com/kitUIN/PicImageSearch/main/demo/images/test02.jpg"
file = open(r"images/test02.jpg", "rb")


@logger.catch()
async def test() -> None:
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
    show_result(resp)


def show_result(resp: BaiDuResponse) -> None:
    # logger.info(resp.origin)  # 原始数据
    logger.info(resp.item)
    if resp.same:  # 存在来源结果
        # logger.info(resp.raw[0].origin)
        logger.info(resp.raw[0].page_title)
        logger.info(resp.raw[0].title)
        logger.info(resp.raw[0].abstract)
        logger.info(resp.raw[0].url)
        logger.info(resp.raw[0].image_src)
        logger.info(resp.raw[0].img_list)
    else:
        logger.info(resp.similar)
    logger.info("-" * 50)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
    # test_sync()
