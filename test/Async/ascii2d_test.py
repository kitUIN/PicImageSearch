import asyncio

from loguru import logger
from PicImageSearch import AsyncAscii2D, NetWork


async def main():
    async with NetWork() as client:
        ascii2d = AsyncAscii2D(client=client, bovw=True)
        res = await ascii2d.search("https://pixiv.cat/77702503-1.jpg")
        # res = await ascii2d.search(r'C:/kitUIN/img/tinted-good.jpg')  # 搜索本地图片
        # logger.info(res.origin)  # 原始数据
        # logger.info(res.raw)  #
        logger.info(
            res.raw[1]
        )  # <NormAscii2D(title=['2020.08.30'], authors=['hews__'],mark=['twitter'])>
        logger.info(
            res.raw[1].thumbnail
        )  # https://ascii2d.net/thumbnail/2/c/5/e/2c5e6a18fbba730a65cef0549e3c5768.jpg
        logger.info(res.raw[1].title)  # 2020.08.30
        logger.info(res.raw[1].authors)  # hews__
        logger.info(
            res.raw[1].url
        )  # https://twitter.com/hews__/status/1299728221005643776
        logger.info(res.raw[1].detail)  # 2570x4096 JPEG 1087.9KB


loop = asyncio.new_event_loop()
loop.run_until_complete(main())
