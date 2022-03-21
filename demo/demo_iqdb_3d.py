from loguru import logger
from PicImageSearch import Network
from PicImageSearch.sync import Iqdb

# proxies = "http://127.0.0.1:1081"
proxies = None
# url = "https://raw.githubusercontent.com/kitUIN/PicImageSearch/main/demo/images/test04.jpg"
url = r"images/test04.jpg"  # 搜索本地图片


@logger.catch()
async def test():
    async with Network(proxies=proxies) as client:
        iqdb = Iqdb(client=client)
        res = await iqdb.search_3d(url)
        # logger.info(res.origin)  # 原始数据
        logger.info(res.raw[0].origin)
        logger.info("说明: " + res.raw[0].content)
        logger.info("来源地址: " + res.raw[0].url)
        logger.info("缩略图: " + res.raw[0].thumbnail)
        logger.info("相似度: " + str(res.raw[0].similarity))
        logger.info("图片大小: " + res.raw[0].size)
        logger.info("图片来源: " + res.raw[0].source)
        logger.info("其他图片来源: " + str(res.raw[0].other_source))
        logger.info("相似度低的结果有多少: " + str(len(res.more)))


if __name__ == "__main__":
    import asyncio

    asyncio.get_event_loop().run_until_complete(test())