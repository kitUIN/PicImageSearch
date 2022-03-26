import asyncio

from loguru import logger

from PicImageSearch import Iqdb, Network
from PicImageSearch.sync import Iqdb as IqdbSync
from PicImageSearch.Utils import IqdbResponse

# proxies = "http://127.0.0.1:1081"
proxies = None
# url = "https://raw.githubusercontent.com/kitUIN/PicImageSearch/main/demo/images/test01.jpg"
url = r"images/test01.jpg"  # 搜索本地图片


@logger.catch()
async def test() -> None:
    async with Network(proxies=proxies) as client:
        iqdb = Iqdb(client=client)
        resp = await iqdb.search(url)
        show_result(resp)


@logger.catch()
def test_sync() -> None:
    iqdb = IqdbSync(proxies=proxies)
    resp = iqdb.search(url)
    show_result(resp)


def show_result(resp: IqdbResponse) -> None:
    # logger.info(resp.origin)  # 原始数据
    logger.info(resp.raw[0].origin)
    logger.info("说明: " + resp.raw[0].content)
    logger.info("来源地址: " + resp.raw[0].url)
    logger.info("缩略图: " + resp.raw[0].thumbnail)
    logger.info("相似度: " + str(resp.raw[0].similarity))
    logger.info("图片大小: " + resp.raw[0].size)
    logger.info("图片来源: " + resp.raw[0].source)
    logger.info("其他图片来源: " + str(resp.raw[0].other_source))
    logger.info("SauceNAO搜图链接: " + resp.saucenao_url)
    logger.info("Ascii2d搜图链接: " + resp.ascii2d_url)
    logger.info("TinEye搜图链接: " + resp.tineye_url)
    logger.info("Google搜图链接: " + resp.google_url)
    logger.info("相似度低的结果有多少: " + str(len(resp.more)))
    logger.info("-" * 50)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
    # test_sync()
