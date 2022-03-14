import asyncio

from loguru import logger
from PicImageSearch import AsyncIqdb, NetWork


async def main():
    async with NetWork() as client:
        iqdb = AsyncIqdb(client=client)
        res = await iqdb.search("https://pixiv.cat/77702503-1.jpg")
        # logger.info(res.origin)
        # logger.info(res.raw)
        logger.info("说明:              " + res.raw[0].content)
        logger.info("来源地址:          " + res.raw[0].url)
        logger.info("缩略图:            " + res.raw[0].thumbnail)
        logger.info("相似度:            " + res.raw[0].similarity)
        logger.info("图片大小:          " + res.raw[0].size)
        logger.info("图片来源:          " + res.raw[0].source)
        logger.info("其他图片来源:      " + str(res.raw[0].other_source))
        logger.info("SauceNAO搜图链接:  " + res.saucenao)
        logger.info("Ascii2d搜图链接:   " + res.ascii2d)
        logger.info("TinEye搜图链接:    " + res.tineye)
        logger.info("Google搜图链接:    " + res.google)
        logger.info("相似度低的结果:    " + str(res.more))


loop = asyncio.new_event_loop()
loop.run_until_complete(main())
