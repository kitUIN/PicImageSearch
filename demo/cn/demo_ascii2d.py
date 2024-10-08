import asyncio

from loguru import logger

from src import Ascii2D, Network
from src.model import Ascii2DResponse
from src.sync import Ascii2D as Ascii2DSync

# proxies = "http://127.0.0.1:1081"
proxies = None
base_url = "https://ascii2d.net"
url = "https://raw.githubusercontent.com/kitUIN/PicImageSearch/main/demo/images/test01.jpg"
file = "../images/test01.jpg"
bovw = False  # 是否使用特征检索
verify_ssl = True  # 是否校验 SSL 证书


@logger.catch()
async def test_async() -> None:
    async with Network(proxies=proxies, verify_ssl=verify_ssl) as client:
        ascii2d = Ascii2D(base_url=base_url, client=client, bovw=bovw)
        # resp = await ascii2d.search(url=url)
        resp = await ascii2d.search(file=file)
        show_result(resp)


@logger.catch()
def test_sync() -> None:
    ascii2d = Ascii2DSync(proxies=proxies, verify_ssl=verify_ssl, bovw=bovw)
    resp = ascii2d.search(url=url)
    # resp = ascii2d.search(file=file)
    show_result(resp)  # type: ignore


def show_result(resp: Ascii2DResponse) -> None:
    # logger.info(resp.origin)  # 原始数据
    logger.info(resp.url)  # 搜索结果链接
    selected = next((i for i in resp.raw if i.title or i.url_list), resp.raw[0])
    logger.info(selected.origin)
    logger.info(selected.thumbnail)
    logger.info(selected.title)
    logger.info(selected.author)
    logger.info(selected.author_url)
    logger.info(selected.url)
    logger.info(selected.url_list)
    logger.info(selected.hash)
    logger.info(selected.detail)
    logger.info("-" * 50)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_async())
    # test_sync()
