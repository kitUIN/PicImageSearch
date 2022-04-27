import asyncio

from loguru import logger

from PicImageSearch import EHentai, Network
from PicImageSearch.model import EHentaiResponse
from PicImageSearch.sync import EHentai as EHentaiSync

proxies = "http://127.0.0.1:1081"
# proxies = None
url = "https://raw.githubusercontent.com/kitUIN/PicImageSearch/main/demo/images/test06.jpg"
file = open(r"images/test06.jpg", "rb")
cookies = None  # 注意：如果要使用 EXHentai 搜索，需要提供 cookies
ex = False  # 是否使用 EXHentai 搜索


@logger.catch()
async def test() -> None:
    async with Network(proxies=proxies, cookies=cookies) as client:
        ehentai = EHentai(client=client)
        # resp = await ehentai.search(url=url, ex=ex)
        resp = await ehentai.search(file=file, ex=ex)
        show_result(resp)


@logger.catch()
def test_sync() -> None:
    ehentai = EHentaiSync(proxies=proxies, cookies=cookies)
    resp = ehentai.search(url=url, ex=ex)
    # resp = ehentai.search(file=file, ex=ex)
    show_result(resp)


def show_result(resp: EHentaiResponse) -> None:
    # logger.info(resp.origin)  # 原始数据
    logger.info(resp.url)  # 搜索结果链接
    # logger.info(resp.raw[0].origin)
    logger.info(resp.raw[0].title)
    logger.info(resp.raw[0].url)
    logger.info(resp.raw[0].thumbnail)
    logger.info(resp.raw[0].type)
    logger.info(resp.raw[0].date)
    logger.info(resp.raw[0].tags)
    logger.info("-" * 50)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
    # test_sync()
