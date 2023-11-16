import asyncio

from loguru import logger

from PicImageSearch import EHentai, Network
from PicImageSearch.model import EHentaiResponse
from PicImageSearch.sync import EHentai as EHentaiSync

proxies = "http://127.0.0.1:1081"
# proxies = None
url = "https://raw.githubusercontent.com/kitUIN/PicImageSearch/main/demo/images/test06.jpg"
file = "images/test06.jpg"

# 注意：如果要使用 EXHentai 搜索，需要提供 cookies (Note: EXHentai search requires cookies if to be used)
cookies = None
# 是否使用 EXHentai 搜索，推荐用 bool(cookies) ，即配置了 cookies 就使用 EXHentai 搜索
# Use EXHentai search or not, it's recommended to use bool(cookies), i.e. use EXHentai search if cookies is configured
ex = False
# 尽可能避免超时返回空的 document (Whenever possible, avoid timeouts that return an empty document)
timeout = 60


@logger.catch()
async def test() -> None:
    async with Network(proxies=proxies, cookies=cookies, timeout=timeout) as client:
        ehentai = EHentai(client=client)
        # resp = await ehentai.search(url=url, ex=ex)
        resp = await ehentai.search(file=file, ex=ex)
        show_result(resp)


@logger.catch()
def test_sync() -> None:
    ehentai = EHentaiSync(proxies=proxies, cookies=cookies, timeout=timeout)
    resp = ehentai.search(url=url, ex=ex)
    # resp = ehentai.search(file=file, ex=ex)
    show_result(resp)  # type: ignore


def show_result(resp: EHentaiResponse) -> None:
    # logger.info(resp.origin)  # 原始数据 (Original data)
    logger.info(resp.url)  # 搜索结果链接 (Link to search results)
    # logger.info(resp.raw[0].origin)
    logger.info(resp.raw[0].title)
    logger.info(resp.raw[0].url)
    logger.info(resp.raw[0].thumbnail)
    logger.info(resp.raw[0].type)
    logger.info(resp.raw[0].date)

    # 推荐使用 Compact / Extended 页面布局，否则拿不到 tags
    # It is recommended to use the Compact / Extended page layout, otherwise you will not get tags
    logger.info(resp.raw[0].tags)
    logger.info("-" * 50)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
    # test_sync()
