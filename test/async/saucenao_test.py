import asyncio

from loguru import logger
from PicImageSearch import NetWork, SauceNAO

# proxies = "http://127.0.0.1:1081"
proxies = None
api_key = "a4ab3f81009b003528f7e31aed187fa32a063f58"


async def main():
    async with NetWork(proxies=proxies) as client:
        saucenao = SauceNAO(api_key=api_key, client=client)
        res = await saucenao.search("https://pixiv.cat/77702503-1.jpg")
        # res = await saucenao.search(r'C:\Users\kulujun\Pictures\90139691_p0.png') #搜索本地图片
        logger.info(res.origin)  # 原始数据
        logger.info(res.raw)  #
        logger.info(res.raw[0])  #
        logger.info(res.long_remaining)  # 99
        logger.info(res.short_remaining)  # 3
        logger.info(
            res.raw[0].thumbnail
        )  # https://img1.saucenao.com/res/pixiv/7770/77702503_p0_master1200.jpg?auth=pJmiu8qNI1z2fLBAlAsx7A&exp=1604748473
        logger.info(res.raw[0].similarity)  # 92.22
        logger.info(res.raw[0].title)  # MDR♡
        logger.info(res.raw[0].author)  # CeNanGam
        logger.info(
            res.raw[0].url
        )  # https://www.pixiv.net/member_illust.php?mode=medium&illust_id=77702503
        logger.info(res.raw[0].pixiv_id)  # 77702503
        logger.info(res.raw[0].member_id)  # 4089680


loop = asyncio.new_event_loop()
loop.run_until_complete(main())
