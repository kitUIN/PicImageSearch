import asyncio

from loguru import logger

from PicImageSearch import Iqdb, Network
from PicImageSearch.model import IqdbResponse
from PicImageSearch.sync import Iqdb as IqdbSync

# proxies = "http://127.0.0.1:1081"
proxies = None
url = "https://raw.githubusercontent.com/kitUIN/PicImageSearch/main/demo/images/test04.jpg"
file = "../images/test04.jpg"


@logger.catch()
async def test_async() -> None:
    async with Network(proxies=proxies) as client:
        iqdb = Iqdb(client=client)
        # resp = await iqdb.search(url=url, is_3d=True)
        resp = await iqdb.search(file=file, is_3d=True)
        show_result(resp)


@logger.catch()
def test_sync() -> None:
    iqdb = IqdbSync(proxies=proxies)
    resp = iqdb.search(url=url, is_3d=True)
    # resp = iqdb.search(file=file, is_3d=True)
    show_result(resp)  # type: ignore


def show_result(resp: IqdbResponse) -> None:
    # logger.info(resp.origin)  # Original Data
    logger.info(resp.url)  # Link to search results
    # logger.info(resp.raw[0].origin)
    logger.info(f"Description: {resp.raw[0].content}")
    logger.info(f"Source URL: {resp.raw[0].url}")
    logger.info(f"Thumbnail: {resp.raw[0].thumbnail}")
    logger.info(f"Similarity: {resp.raw[0].similarity}")
    logger.info(f"Image Size: {resp.raw[0].size}")
    logger.info(f"Image Source: {resp.raw[0].source}")
    logger.info(f"Other Image Sources: {resp.raw[0].other_source}")
    logger.info(f"Number of Results with Lower Similarity: {len(resp.more)}")
    logger.info("-" * 50)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_async())
    # test_sync()
