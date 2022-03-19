from loguru import logger
from PicImageSearch import Network
from PicImageSearch.sync import TraceMoe

# proxies = "http://127.0.0.1:1081"
proxies = None
# url = "https://raw.githubusercontent.com/kitUIN/PicImageSearch/main/demo/images/test05.jpg"
url = r"images/test05.jpg"  # 搜索本地图片


@logger.catch()
async def test():
    async with Network(proxies=proxies) as client:
        tracemoe = TraceMoe(client=client, mute=False, size=None)
        res = await tracemoe.search(url)
        # logger.info(res.origin)  # 原始数据
        logger.info(res.raw[0].origin)
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


if __name__ == "__main__":
    import asyncio

    asyncio.get_event_loop().run_until_complete(test())
