import asyncio

from demo.code.config import IMAGE_BASE_URL, PROXIES, get_image_path, logger
from PicImageSearch import Iqdb, Network
from PicImageSearch.model import IqdbResponse
from PicImageSearch.sync import Iqdb as IqdbSync

url = f"{IMAGE_BASE_URL}/test04.jpg"
file = get_image_path("test04.jpg")


@logger.catch()
async def demo_async() -> None:
    async with Network(proxies=PROXIES) as client:
        iqdb = Iqdb(is_3d=True, client=client)
        # resp = await iqdb.search(url=url)
        resp = await iqdb.search(file=file)
        show_result(resp)


@logger.catch()
def demo_sync() -> None:
    iqdb = IqdbSync(is_3d=True, proxies=PROXIES)
    resp = iqdb.search(url=url)
    # resp = iqdb.search(file=file)
    show_result(resp)  # pyright: ignore[reportArgumentType]


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
    asyncio.run(demo_async())
    # demo_sync()
