import asyncio
from pathlib import Path

from loguru import logger

from PicImageSearch import Ascii2D, Network
from PicImageSearch.model import Ascii2DResponse
from PicImageSearch.sync import Ascii2D as Ascii2DSync

# proxies = "http://127.0.0.1:1080"
proxies = None
base_url = "https://ascii2d.net"
url = "https://raw.githubusercontent.com/kitUIN/PicImageSearch/main/demo/images/test01.jpg"
file = Path(__file__).parent.parent / "images" / "test01.jpg"
bovw = False  # Use feature search or not
verify_ssl = True  # Whether to verify SSL certificates or not


@logger.catch()
async def test_async() -> None:
    async with Network(proxies=proxies, verify_ssl=verify_ssl) as client:
        ascii2d = Ascii2D(base_url=base_url, client=client, bovw=bovw)
        ascii2d = Ascii2D(base_url=base_url, bovw=bovw, client=client)
        # resp = await ascii2d.search(url=url)
        resp = await ascii2d.search(file=file)
        show_result(resp)


@logger.catch()
def test_sync() -> None:
    ascii2d = Ascii2DSync(base_url=base_url, bovw=bovw, proxies=proxies, verify_ssl=verify_ssl)
    resp = ascii2d.search(url=url)
    # resp = ascii2d.search(file=file)
    show_result(resp)  # type: ignore


def show_result(resp: Ascii2DResponse) -> None:
    # logger.info(resp.origin)  # Original data
    logger.info(resp.url)  # Link to search results
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
    asyncio.run(test_async())
    # test_sync()
