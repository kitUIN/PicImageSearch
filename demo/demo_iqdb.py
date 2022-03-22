from loguru import logger

from PicImageSearch import Iqdb, Network

# proxies = "http://127.0.0.1:1081"
proxies = None
# url = "https://raw.githubusercontent.com/kitUIN/PicImageSearch/main/demo/images/test01.jpg"
url = r"images/test01.jpg"  # 搜索本地图片


@logger.catch()
async def test() -> None:
    async with Network(proxies=proxies) as client:
        iqdb = Iqdb(client=client)
        res = await iqdb.search(url)
        # logger.info(res.origin)  # 原始数据
        logger.info(res.raw[0].origin)
        logger.info("说明: " + res.raw[0].content)
        logger.info("来源地址: " + res.raw[0].url)
        logger.info("缩略图: " + res.raw[0].thumbnail)
        logger.info("相似度: " + str(res.raw[0].similarity))
        logger.info("图片大小: " + res.raw[0].size)
        logger.info("图片来源: " + res.raw[0].source)
        logger.info("其他图片来源: " + str(res.raw[0].other_source))
        logger.info("SauceNAO搜图链接: " + res.saucenao_url)
        logger.info("Ascii2d搜图链接: " + res.ascii2d_url)
        logger.info("TinEye搜图链接: " + res.tineye_url)
        logger.info("Google搜图链接: " + res.google_url)
        logger.info("相似度低的结果有多少: " + str(len(res.more)))


if __name__ == "__main__":
    import asyncio

    asyncio.get_event_loop().run_until_complete(test())
