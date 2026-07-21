import asyncio

from demo.code.config import IMAGE_BASE_URL, PROXIES, get_image_path, logger
from PicImageSearch import Iqdb, Network
from PicImageSearch.model import IqdbResponse
from PicImageSearch.sync import Iqdb as IqdbSync

url = f"{IMAGE_BASE_URL}/test01.jpg"
file = get_image_path("test01.jpg")


@logger.catch()
async def demo_async() -> None:
    async with Network(proxies=PROXIES) as client:
        iqdb = Iqdb(client=client)
        # resp = await iqdb.search(url=url)
        resp = await iqdb.search(file=file)
        show_result(resp)


@logger.catch()
def demo_sync() -> None:
    iqdb = IqdbSync(proxies=PROXIES)
    resp = iqdb.search(url=url)
    # resp = iqdb.search(file=file)
    show_result(resp)  # pyright: ignore[reportArgumentType]


def show_result(resp: IqdbResponse) -> None:
    # logger.info(resp.origin)  # Original Data
    logger.info(resp.url)  # Link to search results
    result = resp.raw[0]
    # logger.info(result.origin)
    logger.info(f"Description: {result.content}")
    logger.info(f"Source URL: {result.url}")
    logger.info(f"Thumbnail: {result.thumbnail}")
    logger.info(f"Similarity: {result.similarity}")
    logger.info(f"Image Size: {result.size}")
    logger.info(f"Image Source: {result.source}")
    logger.info(f"Other Image Sources: {result.other_source}")
    logger.info(f"SauceNAO Search Link: {resp.saucenao_url}")
    logger.info(f"Ascii2d Search Link: {resp.ascii2d_url}")
    logger.info(f"TinEye Search Link: {resp.tineye_url}")
    logger.info(f"Google Search Link: {resp.google_url}")
    logger.info(f"Number of Results with Lower Similarity: {len(resp.more)}")
    logger.info("-" * 50)


if __name__ == "__main__":
    asyncio.run(demo_async())
    # demo_sync()
