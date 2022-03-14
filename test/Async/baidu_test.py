import asyncio

from loguru import logger
from PicImageSearch import AsyncBaiDu, NetWork


async def main():
    async with NetWork(proxy="http://127.0.0.1:10809") as client:
        baidu = AsyncBaiDu(client=client)
        res = await baidu.search(
            "https://i0.hdslb.com/bfs/article/e756dd0a8375a4c30cc0ee3a51c8067157486135.jpg@1524w_856h.webp"
        )
        logger.info(res.item)
        logger.info(res.origin)
        if hasattr(res, "same"):  # 存在来源结果
            logger.info(res.raw[0].page_title)
            logger.info(res.raw[0].abstract)
            logger.info(res.raw[0].url)
            logger.info(res.raw[0].image_src)
        else:
            logger.info(res.similar)


loop = asyncio.new_event_loop()
loop.run_until_complete(main())
