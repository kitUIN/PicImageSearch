from loguru import logger

from PicImageSearch import Google, Network

proxies = "http://127.0.0.1:1081"
# proxies = None
# url = "https://raw.githubusercontent.com/kitUIN/PicImageSearch/main/demo/images/test03.jpg"
url = r"images/test03.jpg"  # 搜索本地图片


@logger.catch()
async def test() -> None:
    async with Network(proxies=proxies) as client:
        google = Google(client=client)
        res = await google.search(url)
        # logger.info(res.origin)  # Original Data
        # Should start from index 2, because from there is matching image
        logger.info(res.raw[2].origin)
        logger.info(res.index)
        logger.info(res.raw[2].thumbnail)
        logger.info(res.raw[2].title)
        logger.info(res.raw[2].url)
        logger.info(res.page)
        res2 = await google.goto_page(res.get_page_url(2), 2)
        # logger.info(res2.origin)
        logger.info(res2.raw[2].origin)
        logger.info(res.index)
        logger.info(res2.raw[2].thumbnail)
        logger.info(res2.raw[2].title)
        logger.info(res2.raw[2].url)


if __name__ == "__main__":
    import asyncio

    asyncio.get_event_loop().run_until_complete(test())
