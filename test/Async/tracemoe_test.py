import asyncio

from loguru import logger
from PicImageSearch import AsyncTraceMoe, NetWork


async def main():
    async with NetWork() as client:
        tracemoe = AsyncTraceMoe(mute=False, size=None, client=client)
        res = await tracemoe.search("https://trace.moe/img/tinted-good.jpg")  # 搜索网络图片
        # res = await tracemoe.search(r'C:/Users/kulujun/Pictures/1.png')  # 搜索本地图片
        logger.info(res.origin)
        logger.info(res.raw)
        logger.info(res.raw[0])
        logger.info(res.frameCount)
        logger.info(res.raw[0].anilist)
        logger.info(res.raw[0].idMal)
        logger.info(res.raw[0].title)
        logger.info(res.raw[0].title_native)
        logger.info(res.raw[0].title_romaji)
        logger.info(res.raw[0].title_english)
        logger.info(res.raw[0].title_chinese)
        logger.info(res.raw[0].synonyms)
        logger.info(res.raw[0].isAdult)
        logger.info(res.raw[0].filename)
        logger.info(res.raw[0].episode)
        logger.info(res.raw[0].From)
        logger.info(res.raw[0].To)
        logger.info(res.raw[0].similarity)
        logger.info(res.raw[0].video)
        logger.info(res.raw[0].image)


loop = asyncio.new_event_loop()
loop.run_until_complete(main())
