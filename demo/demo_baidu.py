from loguru import logger

from PicImageSearch import BaiDu, Network

# proxies = "http://127.0.0.1:1081"
proxies = None
# url = "https://raw.githubusercontent.com/kitUIN/PicImageSearch/main/demo/images/test02.jpg"
url = r"images/test02.jpg"  # 搜索本地图片


@logger.catch()
async def test() -> None:
    async with Network(proxies=proxies) as client:
        baidu = BaiDu(client=client)
        res = await baidu.search(url)
        # logger.info(res.origin)  # 原始数据
        logger.info(res.item)
        if res.same:  # 存在来源结果
            logger.info(res.raw[0].origin)
            logger.info(res.raw[0].page_title)
            logger.info(res.raw[0].title)
            logger.info(res.raw[0].abstract)
            logger.info(res.raw[0].url)
            logger.info(res.raw[0].image_src)
            logger.info(res.raw[0].img_list)
        else:
            logger.info(res.similar)


if __name__ == "__main__":
    import asyncio

    asyncio.get_event_loop().run_until_complete(test())
