from loguru import logger

from PicImageSearch import Network, SauceNAO

# proxies = "http://127.0.0.1:1081"
proxies = None
# url = "https://raw.githubusercontent.com/kitUIN/PicImageSearch/main/demo/images/test01.jpg"
url = r"images/test01.jpg"  # 搜索本地图片
api_key = "a4ab3f81009b003528f7e31aed187fa32a063f58"


@logger.catch()
async def test() -> None:
    async with Network(proxies=proxies) as client:
        saucenao = SauceNAO(client=client, api_key=api_key)
        res = await saucenao.search(url)
        # logger.info(res.origin)  # 原始数据
        logger.info(res.raw[0].origin)
        logger.info(res.long_remaining)
        logger.info(res.short_remaining)
        logger.info(res.raw[0].thumbnail)
        logger.info(res.raw[0].similarity)
        logger.info(res.raw[0].title)
        logger.info(res.raw[0].author)
        logger.info(res.raw[0].url)
        logger.info(res.raw[0].pixiv_id)
        logger.info(res.raw[0].member_id)


if __name__ == "__main__":
    import asyncio

    asyncio.get_event_loop().run_until_complete(test())
