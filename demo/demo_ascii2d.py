from loguru import logger

from PicImageSearch import Ascii2D, Network

# proxies = "http://127.0.0.1:1081"
proxies = None
# url = "https://raw.githubusercontent.com/kitUIN/PicImageSearch/main/demo/images/test01.jpg"
url = r"images/test01.jpg"  # 搜索本地图片
bovw = True


@logger.catch()
async def test() -> None:
    async with Network(proxies=proxies) as client:
        ascii2d = Ascii2D(client=client, bovw=bovw)
        res = await ascii2d.search(url)
        # logger.info(res.origin)  # 原始数据
        logger.info(res.raw[1].origin)
        logger.info(res.raw[1].thumbnail)
        logger.info(res.raw[1].title)
        logger.info(res.raw[1].author)
        logger.info(res.raw[1].author_url)
        logger.info(res.raw[1].url)
        logger.info(res.raw[1].detail)
        logger.info(res.raw[1].mark)


if __name__ == "__main__":
    import asyncio

    asyncio.get_event_loop().run_until_complete(test())
